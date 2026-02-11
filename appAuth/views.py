
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from appAuth.conexion import Autenticacion
from appAuth.models import UnidadModel, UsuarioModel
from appTramite.models import ModelControlTramite, ModelRutaTramite

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            usuario = UsuarioModel.objects.filter(username_usuario=username,password_dos_usuario=password).first()
            print(usuario)
            # if usuario and check_password(password, usuario.password_dos_usuario):
            if usuario is not None:
                user = User.objects.get(username=username)
                print(user)
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                # login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                messages.info(request, 'El nombre de Usuario o la contraseña son incorrectas')
    return render(request,'registration/login.html')

def log_out(request):
    logout(request)
    return redirect('login')

gerencias = ['Gerencia General','Gerencia Comercial', 'Gerencia de Planificacion', 'Gerencia de Produccion del Servicio', 'Gerencia de Administración y Recursos Humanos', 'Gerencia de Finanzas']

def index(request):
    tramites = ModelControlTramite.objects.all().order_by('-id')
    rutas = ModelRutaTramite.objects.all()
    usuario = UsuarioModel.objects.filter(username_usuario=request.user.username).first()
    if usuario.unidad_usuario:
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
    # unidad = request.user.groups.first()
    # is_gerencia = False
    is_gerencia = True
    if unidad: 
        if unidad.nombre_unidad.lower() in [gerencia.lower() for gerencia in gerencias]:
            is_gerencia = True
    return render(request, 'index.html',{'is_gerencia':is_gerencia,'tramites':tramites,'rutas':rutas})

