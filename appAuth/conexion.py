from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import UsuarioModel
from ldap3 import Server, Connection, ALL, SUBTREE, NTLM
from ldap3.core.exceptions import LDAPException
import sys
from django.db import DatabaseError


class Autenticacion(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        r"""Authenticate a user against Active Directory using ldap3.

        This replaces the previous python-ldap usage so it works on Windows
        without compiling C extensions. It attempts an NTLM bind using the
        DOMAIN\username form and then searches for commonly used AD attributes.
        """
        # Avoid performing LDAP operations during management commands like
        # `createsuperuser`, `migrate`, etc. This prevents the backend from
        # raising network/db-related errors while running management tasks.
        if any(cmd in sys.argv for cmd in ("createsuperuser", "migrate", "makemigrations", "collectstatic")):
            return None

        if not username or not password:
            return None
        
        ATTRIBUTES_TO_FETCH = ['givenName', 'sn', 'mail', 'memberOf', 'sAMAccountName', 'name', 'distinguishedName']

        LDAP_SERVER = 'ldap://192.9.200.51:389'
        LDAP_USER_BASE = 'dc=comteco,dc=net'
        LDAP_DOMAIN = 'COMTECO'  # adjust as needed (uppercase typical for NTLM)

        user_bind = f"{LDAP_DOMAIN}\\{username}"
        try:
            server = Server(LDAP_SERVER, get_info=ALL)

            # First try NTLM (domain\user). On some Python builds NTLM requires MD4
            # support in hashlib; if that's missing you'll get an "unsupported hash
            # type MD4" error. In that case we fallback to a simple bind using the
            # userPrincipalName (username@domain).
            try:
                conn = Connection(server, user=user_bind, password=password, authentication=NTLM, auto_bind=True)
            except Exception as ntlm_err:
                err_text = str(ntlm_err).lower()
                # Detect MD4-related failure or generic NTLM failure and fallback
                if 'md4' in err_text or 'unsupported hash' in err_text or 'ntlm' in err_text:
                    # Fallback to simple bind with userPrincipalName
                    try:
                        user_principal = f"{username}@comteco.net"
                        conn = Connection(server, user=user_principal, password=password, auto_bind=True)
                    except Exception as simple_err:
                        # Both NTLM and simple bind failed; re-raise so outer handler logs.
                        raise simple_err
                else:
                    # Unexpected NTLM error, re-raise
                    raise ntlm_err

            search_filter = f"(sAMAccountName={username})"
            conn.search(search_base=LDAP_USER_BASE, search_filter=search_filter, search_scope=SUBTREE, attributes=ATTRIBUTES_TO_FETCH)

            if not conn.entries:
                # bind succeeded but user not found in search base
                return self.user_login(username=username, password=password, firstname='', lastname='', email=f"{username}@comteco.com.bo", groups_ldap=[])

            entry = conn.entries[0]

            # Safely extract attributes; ldap3 returns Entry objects where attributes can be accessed by name
            firstname = str(entry.givenName) if 'givenName' in entry else ''
            lastname = str(entry.sn) if 'sn' in entry else ''
            email = str(entry.mail) if 'mail' in entry else ''
            groups_ldap = [str(g) for g in entry.memberOf] if 'memberOf' in entry else []

            return self.user_login(username=username, password=password, firstname=firstname, lastname=lastname, email=email, groups_ldap=groups_ldap)

        except LDAPException as e:
            # LDAP connection/search error
            print(f"LDAP error: {e}")
            return None
        except Exception as e:
            # Other errors
            print(f"Unexpected error during LDAP auth: {e}")
            return None

    def user_login(self, username, password, firstname, lastname, email, groups_ldap):
        """Create or update a Django User and the custom UsuarioModel.

        We do not store plaintext passwords for LDAP users; instead mark the
        Django user as having an unusable password so authentication always
        goes through the LDAP backend.
        """
        # Find or create Django user. Wrap DB operations to avoid crashing
        # management commands if the DB isn't ready yet.
        try:
            user, created = User.objects.get_or_create(username=username)
            user.first_name = firstname or ''
            user.last_name = lastname or ''
            user.email = email or ''
            # Do not set raw password; use unusable password for LDAP-managed accounts
            user.set_unusable_password()
            user.is_active = True
            user.save()

            # Sync/ensure the custom UsuarioModel exists
            usuario, _ = UsuarioModel.objects.get_or_create(username_usuario=username)
            usuario.firstname_usuario = firstname or ''
            usuario.lastname_usuario = lastname or ''
            usuario.email_usuario = email or ''
            # Do not store plaintext LDAP password
            usuario.password_usuario = user.password
            usuario.save()
        except DatabaseError as e:
            # If DB isn't available (e.g., during initial migrations), don't crash.
            # Log and return None so management commands can continue.
            print(f"Database error while syncing LDAP user: {e}")
            return None

        # (Optional) Map groups_ldap -> Django groups here if desired

        return user
