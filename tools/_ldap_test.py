import os
import sys

# Ensure project root is on sys.path so DJANGO_SETTINGS_MODULE can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tramites.settings')
import django

django.setup()

from appAuth.conexion import Autenticacion

username = 'bflores'
password = os.environ.get('LDAP_TEST_PW')

backend = Autenticacion()
user = backend.authenticate(None, username=username, password=password)

if user:
    print('AUTH_SUCCESS')
else:
    print('AUTH_FAILED')
