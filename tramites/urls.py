"""
URL configuration for att project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from appAuth.views import log_in, log_out, index
from appTramite import views
from appTramite.views import finalizar_tramite_view, obtener_ultimo_correlativo, obtener_ultimo_correlativo_documento, pdf_documento, servir_pdf_en_linea, aprobar_jerarquia_view
from django.conf import settings # Importar settings
from django.conf.urls.static import static # Importar la función stati
# from appBpm.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', log_in, name='login'),
    path('logout/', login_required(log_out), name='logout'),
    path('', login_required(index), name='index'),
    ###############################################################################################################
    # URLs para tramite
    ###############################################################################################################
    path('tramites/', login_required(views.ControlTramiteListView.as_view()), name='listcontrol'),
    path('tramites/nuevo/', login_required(views.ControlTramiteCreateView.as_view()), name='createcontrol'),
    
    path('tramites/nuevo/<int:documento_pk>', login_required(views.ControlTramiteDocumentoCreateView.as_view()), name='control_documento_create'),

    path('tramites/derivar/<int:pk>/', login_required(views.RutaTramiteCreateView.as_view()), name='derivartramite'),
    path('tramites/aprobar/<int:pk>/', login_required(aprobar_jerarquia_view), name='aprobacionjerarquia'),
    path('tramites/aprobacion/', login_required(views.AprobacionControlTramiteListView.as_view()), name='aprobacioncontrol'),
    path('tramites/detailview/<int:pk>/', login_required(views.ControlTramiteDetailView.as_view()), name='detailviewcontrol'),
    path('tramites/detail/<int:pk>/', login_required(views.ControlTramiteDetailView.as_view()), name='detailcontrol'),
    path('tramites/finalizar/<int:pk>', login_required(finalizar_tramite_view), name='finalizarcontrol'),
    path('documento/visualizar/<int:pk>/', login_required(servir_pdf_en_linea), name='servir_pdf_en_linea'),
    path('tramites/recepcionar/<int:pk>/', login_required(views.resepcionar_tramite_view), name='recepcionar_tramite'),
    ###############################################################################################################
    # URLs auxiliares para el tramite
    ###############################################################################################################
    path('ajax/get-correlativo/', obtener_ultimo_correlativo, name='get_correlativo'),
    path('ajax/get-correlativo-documento/', obtener_ultimo_correlativo_documento, name='get_correlativo_documento'),


    ###############################################################################################################
    # URLs para BPM
    ###############################################################################################################
    # path('bpm/', BPMListView.as_view(), name='bpm_list'),
    # path('bpm/crear/', BPMCreateView.as_view(), name='bpm_create'),
    # path('bpm/<int:pk>/', BPMDetailView.as_view(), name='bpm_detail'),
    # path('bpm/<int:pk>/editar/', BPMUpdateView.as_view(), name='bpm_update'),
    ###############################################################################################################
    # URLs para Tarea
    ###############################################################################################################
    # path('tarea/', TareaListView.as_view(), name='tarea_list'),
    # path('tarea/crear/<int:pk>/', login_required(TareaCreateView.as_view()), name='tarea_create'),
    # path('tarea/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    # path('tarea/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_update'),

    path('documento/', login_required(views.DocumentoListView.as_view()), name='documento_list'),
    path('documento/nuevo/', login_required(views.DocumentoCreateView.as_view()), name='documento_create'),
    path('documento/<int:pk>/', login_required(views.DocumentoDetailView.as_view()), name='documento_detail'),
    path('documento/<int:pk>/editar/', login_required(views.DocumentoUpdateView.as_view()), name='documento_update'),
    path('documento/<int:pk>/pdf/', login_required(views.exportar_pdf), name='documento_pdf'),
    path('documento/visualizar/<int:pk>/', login_required(pdf_documento), name='documento_ver_pdf'),
]

if settings.DEBUG:
    # Solo en desarrollo, le decimos a Django cómo servir los archivos Media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)