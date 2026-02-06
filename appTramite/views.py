from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from appAuth.models import UnidadModel, UsuarioModel
from .models import DocumentoModel, ModelControlTramite, ModelRutaTramite
from .forms import ControlTramiteDocumentoForm, ControlTramiteForm, DocumentoForm, RutaTramiteForm
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
import logging
import os

logger = logging.getLogger(__name__)

# Creacion de variables globales
gerencias = [
    'gerencia general',
    'gerencia comercial', 
    'gerencia de planificacion', 
    'gerencia de produccion', 
    'gerencia de administracion de finanzas',
    'consejo de administracion']
abecedario = [{'acronimo_unidad': 'A', 'nombre_unidad': 'Letra A'},
              {'acronimo_unidad': 'B', 'nombre_unidad': 'Letra B'},
              {'acronimo_unidad': 'C', 'nombre_unidad': 'Letra C'},
              {'acronimo_unidad': 'D', 'nombre_unidad': 'Letra D'},
              {'acronimo_unidad': 'E', 'nombre_unidad': 'Letra E'},
              {'acronimo_unidad': 'F', 'nombre_unidad': 'Letra F'},
              {'acronimo_unidad': 'G', 'nombre_unidad': 'Letra G'},
              {'acronimo_unidad': 'H', 'nombre_unidad': 'Letra H'},
              {'acronimo_unidad': 'I', 'nombre_unidad': 'Letra I'},
              {'acronimo_unidad': 'J', 'nombre_unidad': 'Letra J'},
              {'acronimo_unidad': 'K', 'nombre_unidad': 'Letra K'},
              {'acronimo_unidad': 'L', 'nombre_unidad': 'Letra L'},
              {'acronimo_unidad': 'M', 'nombre_unidad': 'Letra M'},
              {'acronimo_unidad': 'N', 'nombre_unidad': 'Letra N'},
              {'acronimo_unidad': 'O', 'nombre_unidad': 'Letra O'},
              {'acronimo_unidad': 'P', 'nombre_unidad': 'Letra P'},
              {'acronimo_unidad': 'Q', 'nombre_unidad': 'Letra Q'},
              {'acronimo_unidad': 'R', 'nombre_unidad': 'Letra R'},
              {'acronimo_unidad': 'S', 'nombre_unidad': 'Letra S'},
              {'acronimo_unidad': 'T', 'nombre_unidad': 'Letra T'},
              {'acronimo_unidad': 'U', 'nombre_unidad': 'Letra U'},
              {'acronimo_unidad': 'V', 'nombre_unidad':  'Letra V'},
              {'acronimo_unidad':  'W', 'nombre_unidad':  'Letra W'},
              {'acronimo_unidad':  'X',  'nombre_unidad':  'Letra X'},
              {'acronimo_unidad':  'Y',  'nombre_unidad':  'Letra Y'},
              {'acronimo_unidad':  'Z',  'nombre_unidad':  'Letra Z'}]
###############################################################################################################
# ListView Control
###############################################################################################################
class ControlTramiteListView(ListView):
    # 1. Definir el modelo a listar
    model = ModelControlTramite
    # 2. Definir el template HTML que usará para renderizar la lista
    template_name = 'tramites/controltramite_list.html'
    # 3. Definir el nombre de la variable de contexto que contendrá la lista
    # Por defecto, Django usa 'object_list' o 'modelcontroltramite_list' (nombre_modelo_list)
    context_object_name = 'tramites'
    # 4. Opcional: Paginación
    paginate_by = 10 # Muestra 10 trámites por página
    # 5. Opcional: Sobrescribir el queryset para ordenar o filtrar  
    def get_queryset(self):
        # 1. obtenemos el modelo a listar
        queryset = super().get_queryset()
        # 2. obtnemos el usuario logueado
        usuario = self.request.user
        # 3. realizamo la consulta obteniendo solo los tramites correspondientes al usuario logueado
        queryset = queryset.filter(nombre_empleado_control=usuario)
        # 4. Ordena por código_control de forma ascendente
        return queryset.order_by('-id')
        # Alternativamente: ordenar por la fecha más reciente: return ModelControlTramite.objects.all().order_by('-fecha_ini_control')

    def get_context_data(self, **kwargs):
        """Añade el formulario de creación al contexto para que el modal funcione."""
        context = super().get_context_data(**kwargs)
        # verificamos si el usuario pertenece a una gerencia
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        # unidad = self.request.user.groups.first()
        context['is_gerencia'] = False
        if usuario.unidad_usuario.nombre_unidad.lower() in gerencias:
            context['is_gerencia'] = True

        # if unidad.nombre_unidad.lower() in [gerencia.lower() for gerencia in gerencias]:
        #     context['is_gerencia'] = True
        # enviamos todos los modelos ModelRutaTramite para despues depurarlos segun el forekey
        rutas = ModelRutaTramite.objects.all
        context['rutas'] = rutas
        #
        return context

######################################################################################################
# class Createview Control
######################################################################################################
class ControlTramiteCreateView(CreateView):
    """
    Vista Basada en Clases para crear un nuevo ModelControlTramite.
    Utiliza el formulario ControlTramiteForm para la entrada de datos.
    """
    model = ModelControlTramite
    form_class = ControlTramiteForm # Usa el formulario personalizado
    template_name = 'tramites/controltramite_create.html' # Nuevo template específico para el modal
    success_url = reverse_lazy('listcontrol') # Redirige de vuelta a la lista tras guardar exitosamente
    # Función para asignar valores iniciales al formulario
    def get_initial(self):
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        initial = super().get_initial()
        initial['fecha_ini_control']=datetime.today()
        initial['gerencia_codigo_control']=usuario.unidad_usuario.acronimo_unidad
        initial['anio_codigo_control']=datetime.now().year
        
        return initial
    # función para agregar datos al contexto
    def get_context_data(self, **kwargs):
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()

        #  Obtener todas las unidades activas ordenadas por nombre
        unidades = UnidadModel.objects.filter(estado_unidad=True).order_by('nombre_unidad')
        misunidades = []
        # Construir la lista de diccionarios para el contexto
        for unidad in unidades:
            misunidades.append({'acronimo_unidad': unidad.acronimo_unidad, 'nombre_unidad': unidad.nombre_unidad})
        # Agregar las letras del abecedario al final de la lista
        misunidades += abecedario
        #  Obtener el contexto base
        context = super().get_context_data(**kwargs)
        # Agregar datos adicionales al contexto
        context['unidad_usuario'] = usuario.unidad_usuario.acronimo_unidad
        # Agregar la lista de unidades al contexto
        context['unidades'] = misunidades
        return context
    # función para validar el formulario
    def form_valid(self, form):
        """
        Sobrescribe para agregar lógica antes de guardar si es necesario.
        En este caso, simplemente llama al método padre.
        """
        # 1. Agregar valores adicionales antes de guardar
        form.instance.fecha_ini_control = datetime.today()
        # 2. Asignar el usuario actual como nombre_empleado_control
        form.instance.nombre_empleado_control = self.request.user
        # 3. Construir el código_control completo
        form.instance.codigo_control = f"{form.instance.gerencia_codigo_control}-{form.instance.unidad_destino_codigo_control}-{form.instance.anio_codigo_control}-{form.instance.numero_secuencial_codigo_control}"
        # 4. Asignar origen y destino de la ruta igual a la unidad del usuario que crea el trámite
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        # 5. Asignar origen y destino igual a la unidad del usuario
        form.instance.origen_ruta_control = unidad
        form.instance.destino_ruta_control = unidad

        # 6. Guardar el objeto principal (ControlTramite)
        # Esto le asigna un PK (self.object.pk) y guarda los campos simples.
        response = super().form_valid(form)
        # 7. Retornar la respuesta del padre
        return response
    
    def form_invalid(self, form):
        """🔹 Lógica cuando el formulario es inválido"""
        # Log del error
        logger.warning(
            f"Formulario inválido - User: {self.request.user} - "
            f"Errores: {form.errors}"
        )
        
        # Mensaje de error personalizado
        messages.error(
            self.request,
            'Por favor corrige los errores en el formulario.'
        )
        return super().form_invalid(form)

###########################################################################################################
# Crear ControlTramite para documento existente
###########################################################################################################
class ControlTramiteDocumentoCreateView(CreateView):
    model = ModelControlTramite
    form_class = ControlTramiteDocumentoForm
    template_name = 'tramites/controltramite_documento_create.html'
    success_url = reverse_lazy('listcontrol')

    def get_initial(self):
        initial = super().get_initial()
        documento_pk = self.kwargs.get('documento_pk')
        documento = get_object_or_404(DocumentoModel, pk=documento_pk)
        
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        # codigo de control
        initial['gerencia_codigo_control'] = usuario.unidad_usuario.acronimo_unidad
        initial['unidad_destino_codigo_control'] = usuario.unidad_usuario.acronimo_unidad
        initial['anio_codigo_control'] = datetime.now().year
        # fecha de inicio
        initial['fecha_ini_control'] = datetime.today()
        # asunto de control
        initial['asunto_control'] = documento.titulo_documento
        # tipo de control
        initial['tipo_control'] = documento.tipo_documento
        # cite de documento en el control
        initial['nota_control'] = documento.cite_documento
        # origen del documento para el control
        initial['origen_control'] = usuario.unidad_usuario
        # destino del documento para el control
        initial['destino_ruta_control'] = documento.destinatario_documento.unidad_usuario
        
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documento_pk = self.kwargs.get('documento_pk')
        documento = get_object_or_404(DocumentoModel, pk=documento_pk)
        context['documento'] = documento
        return context

    def form_valid(self, form):
        documento_pk = self.kwargs.get('documento_pk')
        documento = get_object_or_404(DocumentoModel, pk=documento_pk)

        # 1. Agregar valores adicionales antes de guardar
        form.instance.fecha_ini_control = datetime.today()
        # 2. Asignar el usuario actual como nombre_empleado_control
        form.instance.nombre_empleado_control = self.request.user
        # 3. Construir el código_control completo
        form.instance.codigo_control = f"{form.instance.gerencia_codigo_control}-{form.instance.unidad_destino_codigo_control}-{form.instance.anio_codigo_control}-{form.instance.numero_secuencial_codigo_control}"
        # 4. Asignar origen y destino de la ruta igual a la unidad del usuario que crea el trámite
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        # 5. Asignar origen y destino igual a la unidad del usuario
        form.instance.origen_ruta_control = usuario.unidad_usuario

        path_de_usuario = obtener_ruta_organigrama(usuario.id,documento.destinatario_documento.id)
        form.instance.path_jerarquia_control = path_de_usuario
        usuario_index = path_de_usuario.index(usuario)

        # Asignamos al jefe del usuario para el seguimiento jerarquico
        form.instance.usuario_jerarquia_control = path_de_usuario[usuario_index+1]
        # Asignamos la unidad del jefe del usuario para el seguimiento jerarquico
        form.instance.destino_jerarquia_control = usuario.gerente_usuario.unidad_usuario
        
        
        

        # 6. Guardar el objeto principal (ControlTramite)
        # Esto le asigna un PK (self.object.pk) y guarda los campos simples.
        response = super().form_valid(form)
        # 7. El control de tramite recién creado
        control_tramite = self.object 
        # 8. Actualizar el documento para vincularlo con el control de tramite
        documento_pk = self.kwargs.get('documento_pk')
        documento = get_object_or_404(DocumentoModel, pk=documento_pk)
        documento.bpm_control_documento = control_tramite
        documento.save()

        # 9. Crear la ruta inicial para el control de tramite
        ruta_inicial = ModelRutaTramite.objects.create(
            control_tramite=control_tramite,
            fecha_ini_ruta=datetime.today(),
            origen_ruta=control_tramite.origen_control,
            destino_ruta=control_tramite.destino_jerarquia_control,

            origen_nombre_empleado=self.request.user.username,
            destino_nombre_empleado=control_tramite.usuario_jerarquia_control.username_usuario,

            estado_ruta=False,

            tipo_ruta = "REVISION" if control_tramite.destino_jerarquia_control == control_tramite.destino_ruta_control else "CONTROL"
        )

        ruta_inicial.save()

        return response


###########################################################################################################
# DetailView ControlTramite
###########################################################################################################
class ControlTramiteDetailView(DetailView):
    model = ModelControlTramite
    template_name = 'tramites/controltramite_detail.html'
    context_object_name = 'tramite'

    def get_context_data(self, **kwargs):
        # obtenemos el contexto
        context = super().get_context_data(**kwargs)
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        context['usuario'] = usuario
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        context['is_gerencia'] = False

        # verificamos si el usuario pertenece a una gerencia para habilitar la opcion MisTramites del menu
        if usuario.unidad_usuario.nombre_unidad.lower() in gerencias:
            context['is_gerencia'] = True
        # if unidad.nombre_unidad.lower() in [gerencia.lower() for gerencia in gerencias]:
        #     context['is_gerencia'] = True

        # obtenemos el model 
        control_pk = self.object.pk
        #obtenemos los objetos rutas q tiene como llave foranea el model
        rutas = ModelRutaTramite.objects.filter(control_tramite=control_pk)
        # adicionames en el contexto todas las rutas encontradas
        context['rutas'] = rutas.order_by()
        ruta = rutas.filter(fecha_resepcion_ruta = None)
        if ruta.exists():
            context['resepcionado'] = False
        else:
            context['resepcionado'] = True
        # retornamos el contexto
        return context
    def get_template_names(self):
        return super().get_template_names()

###########################################################################################################
# class Ruta CreateView
###########################################################################################################
class RutaTramiteCreateView(CreateView):
    model = ModelRutaTramite
    form_class = RutaTramiteForm
    template_name = 'tramites/rutatramite_create.html'
    success_url = reverse_lazy('aprobacioncontrol')

    def get_initial(self):
        """
        Asigna el ID del ModelControlTramite (pk de la URL) como valor inicial 
        para el campo 'control_tramite' del formulario RutaTramiteForm.
        """
        initial = super().get_initial()
        
        # Obtener el PK de la URL
        control_tramite_pk = self.kwargs.get('pk') 
        # Asignar el ID al campo ForeignKey del formulario
        # (El formulario acepta el ID aunque el campo sea un objeto ForeignKey)
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
    
        if control_tramite_pk:
             initial['control_tramite'] = control_tramite_pk
             initial['fecha_ini_ruta'] = datetime.today()
             initial['origen_ruta'] = unidad
             initial['origen_nombre_empleado'] = self.request.user
             
        return initial
    
    def get_context_data(self, **kwargs):
        """
        Añade el objeto ControlTramite padre al contexto para usarlo en el template.
        """
        context = super().get_context_data(**kwargs)
        control_tramite_pk = self.kwargs.get('pk')
        
        # Obtener el objeto padre y pasarlo al template
        if control_tramite_pk:
            context['tramite'] = get_object_or_404(
                ModelControlTramite, 
                pk=control_tramite_pk
            )
        return context
    
    def form_valid(self, form):
        control_tramite_pk = self.kwargs.get('pk')
        ruta_anterior = ModelRutaTramite.objects.filter(Q(control_tramite=control_tramite_pk) & Q(estado_ruta=False))
        if ruta_anterior.exists():
            ruta_anterior = ruta_anterior.first()
            ruta_anterior.estado_ruta = True
            ruta_anterior.fecha_fin_ruta = datetime.today()
            ruta_anterior.destino_nombre_empleado = self.request.user.username
            ruta_anterior.save()

        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        
        control_tramite = ModelControlTramite.objects.get(id=control_tramite_pk)
        form.instance.estado_ruta = False
        form.instance.fecha_ini_ruta = datetime.today()
        form.instance.control_tramite = control_tramite
        form.instance.origen_ruta = unidad
        form.instance.origen_nombre_empleado = self.request.user.username

        usuario_destino = form['usuario_destino_ruta']


        control_tramite.destino_ruta_control = form.instance.destino_ruta
        usuario_index = control_tramite.path_jerarquia_control.index(usuario)
        if len(control_tramite.path_jerarquia_control)-1 > usuario_index:
            control_tramite.destino_jerarquia_control = control_tramite.path_jerarquia_control[usuario_index+1]
        else:
            control_tramite.path_jerarquia_control = obtener_ruta_organigrama(usuario.id,usuario_destino)
        control_tramite.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print('Formulario invalido')
        """🔹 Lógica cuando el formulario es inválido"""
        # Log del error
        logger.warning(
            f"Formulario inválido - User: {self.request.user} - "
            f"Errores: {form.errors}"
        )
        
        # Mensaje de error personalizado
        messages.error(
            self.request,
            'Por favor corrige los errores en el formulario.'
        )
        return super().form_invalid(form)
    def post(self, request, *args, **kwargs):

        control_tramite_pk = self.kwargs.get('pk')

        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()

        # unidad = self.request.user.groups.first()

        form = request.POST.copy()
        
        form['fecha_ini_ruta'] = datetime.today()
        form['control_tramite'] = control_tramite_pk
        form['estado_ruta'] = False
        form['origen_ruta'] = unidad
        form['origen_nombre_empleado'] = self.request.user
        request.POST = form

        return super().post(request, *args, **kwargs)


##########################################################################################################
# Lista de Aprobaciones
##########################################################################################################
class AprobacionControlTramiteListView(ListView):
    model = ModelControlTramite
    template_name = 'tramites/aprobaciontramite_list.html'
    context_object_name = 'tramites' 

    def get_queryset(self):
        # 1. Obtener el QuerySet base (todos los trámites)
        queryset = super().get_queryset()
        
        # 2. Obtener los valores de filtro de los parámetros de la URL (?param=valor)
        estado_filtro = False
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()

        destino_filtro = unidad
        # 3. Aplicar los filtros condicionalmente
        
        rutas_tramites = ModelRutaTramite.objects.filter(estado_ruta=False)

        # Filtrar por destino_ruta_control
        if destino_filtro:
            # Aquí se asume que 'destino_unidad_control' es el campo real en ModelControlTramite

            # queryset = queryset.filter(destino_ruta_control=destino_filtro)
            queryset = queryset.filter(destino_jerarquia_control=destino_filtro)
        # Filtrar por estado_ruta_control (asumiendo que es un campo del modelo)
        # Uso de 'iexact' para búsqueda insensible a mayúsculas/minúsculas o 'exact'
        # Si el campo es un BooleanField, asegúrate de convertir 'estado_filtro' a True/False
        # Por ejemplo: if estado_filtro.lower() == 'activo':
        queryset = queryset.filter(usuario_jerarquia_control=usuario) 
        queryset = queryset.filter(estado_ruta_control=estado_filtro) 
        queryset = queryset.filter(estado_control=estado_filtro)
            
        # 4. Devolver el QuerySet filtrado
        # Opcional: Añadir una ordenación predeterminada si no hay una en Meta
        return queryset.order_by('-id')
    
    def get_context_data(self, **kwargs):
        #
        context =  super().get_context_data(**kwargs)
        #
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        unidad = UnidadModel.objects.filter(id=usuario.unidad_usuario.id).first()
        context['is_gerencia'] = False
        # verificamos si el usuario pertenece a una gerencia
        if usuario.unidad_usuario.nombre_unidad.lower() in gerencias:
            context['is_gerencia'] = True

        # if unidad:
        #     if unidad.nombre_unidad.lower() in [gerencia.lower() for gerencia in gerencias]:
        #         context['is_gerencia'] = True
        # else:
        #     context['is_gerencia'] = False

        # enviamos todos los modelos ModelRutaTramite para despues depurarlos segun el forekey
        rutas = ModelRutaTramite.objects.all()
        context['rutas'] = rutas
        return context
    

#####################################################################################################
# clase update control tramite para finalizar el tramite
#####################################################################################################
class ControlTramiteUpdateView(UpdateView):
    model = ModelControlTramite
    form_class = ControlTramiteForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        print('Formulario Valido')
        try:
            control_tramite = ModelControlTramite.objects.get(pk=self.object.pk)
            datos_originales = self._obtener_datos_originales(control_tramite)
            # 🔷 Guardar el objeto
            self.object = form.save(commit=False)
            self.object.fecha_fin_control = datetime.today()
            self.object.estado_control = True
            # 🔷 Guardar el objeto hijo Model_ruta_tramite
            try:
                rutas = ModelRutaTramite.objects.filter(Q(control_tramite=control_tramite) & Q(estado_ruta=False))
                ruta = rutas.first()
                ruta.estado_ruta = True
                ruta.fecha_fin_ruta = datetime.today()
                ruta.destino_nombre_empleado = self.request.user.get_username()
                ruta.save()
            except Exception as e:
                logger.error(f"Error actualizando artículo {self.object.id}: {str(e)}")
                messages.error(self.request, 'Error interno al guardar los cambios')
                return self.form_invalid(form)
            # 🔷 Guardar cambios
            self.object.save()
            form.save_m2m()
            # 🔷 Enviamos datos a la clase super
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error actualizando artículo {self.object.id}: {str(e)}")
            messages.error(self.request, 'Error interno al guardar los cambios')
            return self.form_invalid(form)
    #
    def form_invalid(self, form):
        print('Formulario Invalido')
        return super().form_invalid(form)

#####################################################################################################
# class Documento list view
#####################################################################################################
class DocumentoListView(ListView):
    model = DocumentoModel
    template_name = 'documentos/documento_list.html'
    context_object_name = 'documentos'
    
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

#####################################################################################################
# class Documento detail view
#####################################################################################################
class DocumentoDetailView(DetailView):
    model = DocumentoModel
    template_name = 'documentos/documento_detail.html'
    context_object_name = 'documento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documento = self.object

        if not documento.bpm_control_documento:
            print('El documento no tiene un trámite asociado.')
            return context
        else:
            tramite = get_object_or_404(ModelControlTramite, pk=documento.bpm_control_documento.pk)
            print('Trámite relacionado:', tramite)
            rutas = ModelRutaTramite.objects.filter(control_tramite=tramite)
            context['rutas'] = rutas
        return context

#####################################################################################################
# class Documento create view
#####################################################################################################
class DocumentoCreateView(CreateView):
    model = DocumentoModel
    form_class = DocumentoForm
    template_name = 'documentos/documento_form.html'
    success_url = reverse_lazy('documento_list')
    def get_initial(self):
        initial = super().get_initial()
        initial['anio_documento'] = datetime.today().year
        initial['unidad_documento'] = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first().unidad_usuario.acronimo_unidad
        return initial   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = UsuarioModel.objects.filter(username_usuario=self.request.user.username).first()
        context['usuario'] = usuario
        return context
    def form_valid(self, form):
        print('Formulario Valido')
        form.instance.usuario_creador_documento = self.request.user
        return super().form_valid(form)
    def form_invalid(self, form):
        print('Formulario Invalido')
        print(form.errors)
        return super().form_invalid(form)

#####################################################################################################
# class Documento update view
#####################################################################################################
class DocumentoUpdateView(UpdateView):
    model = DocumentoModel
    form_class = DocumentoForm
    template_name = 'documentos/documento_form.html'
    success_url = reverse_lazy('documento_list')

#####################################################################################################
# Funciones complementarias
#####################################################################################################
# Función para recepcionar el trámite
def resepcionar_tramite_view(request, pk):
    try:
        ruta = get_object_or_404(ModelRutaTramite, Q(control_tramite=pk) & Q(estado_ruta=False))
        ruta.fecha_resepcion_ruta = datetime.now()
        ruta.save()
        messages.success(request, f'Se ha recepcionado el trámite correctamente.')
        return redirect('detailviewcontrol', pk=pk)
    except Exception as e:
        messages.error(request, f'Ocurrió un error al recepcionar el trámite: {e}')
        return redirect('detailviewcontrol', pk=pk)
    
def aprobar_jerarquia_view(request, pk):
    if request.method == 'POST':

        observacion = request.POST.get('observacion')
        print(observacion)
        usuario = UsuarioModel.objects.filter(username_usuario=request.user.username).first()
        control_tramite = get_object_or_404(ModelControlTramite, pk=pk)
        print(control_tramite)
        try:
            control_tramite.usuario_jerarquia_control = usuario.gerente_usuario
            control_tramite.destino_jerarquia_control = usuario.gerente_usuario.unidad_usuario
            control_tramite.save()
            try:
                ruta = ModelRutaTramite.objects.filter(Q(control_tramite=control_tramite) & Q(estado_ruta=False)).first()
                ruta.estado_ruta = True
                ruta.fecha_fin_ruta = datetime.today()
                ruta.destino_nombre_empleado = request.user.get_username()
                ruta.instruccion_complementaria = observacion
                ruta.save()

            except Exception as e:
                messages.error(request, f'Ocurrió un error al finalizar el trámite: {e}')
                return redirect('detailcontrol', pk=pk) # O la URL de donde vino
            
            nueva_ruta = ModelRutaTramite.objects.create(
                control_tramite=control_tramite,
                fecha_ini_ruta=datetime.today(),
                origen_ruta=usuario.unidad_usuario.nombre_unidad,
                destino_ruta=usuario.gerente_usuario.unidad_usuario,

                origen_nombre_empleado=usuario.username_usuario,
                destino_nombre_empleado=usuario.gerente_usuario.username_usuario,

                estado_ruta=False,

                tipo_ruta = "REVISION" if control_tramite.destino_jerarquia_control == control_tramite.destino_ruta_control else "CONTROL"
            )
            print("La nueva ruta creada por jerarquia",nueva_ruta)
            nueva_ruta.save()
            # Opcional: Notificación
            messages.success(request, f'El Trámite #{control_tramite.codigo_control} ha sido aceptado por { usuario.username_usuario }.')
            # Redirigir a la lista o a otra página
            return redirect('index') 

        except Exception as e:
            messages.error(request, f'Ocurrió un error al finalizar el trámite: {e}')
            return redirect('detailcontrol', pk=pk) # O la URL de donde vino

    return render
# funcion para obtner la ruta de un usuario_A al usuario_B
def obtener_ruta_organigrama(id_usuario_a ,id_usuario_b):
    usuario_a = UsuarioModel.objects.get(pk=id_usuario_a)
    usuario_b = UsuarioModel.objects.get(pk=id_usuario_b)
    print(usuario_a)
    print(usuario_b)
    ruta_1 = []
    usuario_organigrama = usuario_a
    print("soy el jefe: ",usuario_organigrama.gerente_usuario.id)
    while usuario_organigrama:
        ruta_1.append(usuario_organigrama)
        if usuario_organigrama.gerente_usuario:
            usuario_organigrama = UsuarioModel.objects.get(pk=usuario_organigrama.gerente_usuario.id)
        else:
            break
        print(usuario_organigrama)
        # usuario_organigrama = usuario_organigrama.gerente_usuario
    
    ruta_2 = []
    usuario_organigrama = usuario_b
    while usuario_organigrama:
        ruta_2.append(usuario_organigrama)
        if usuario_organigrama.gerente_usuario:
            usuario_organigrama = UsuarioModel.objects.get(pk=usuario_organigrama.gerente_usuario.id)
        else:
            break
        # usuario_organigrama = usuario_organigrama.gerente_usuario
    lca = None
    for user in ruta_1:
        if user in ruta_2:
            lca = user
            break
    if not lca:
        return None # No están en el mismo organigrama
    # 4. Construir la ruta final
    # Camino de A hasta el LCA (subiendo)
    camino_subida = []
    for user in ruta_1:
        camino_subida.append(user)
        if user == lca:
            break

    # Camino del LCA hasta B (bajando)
    camino_bajada = []
    for user in ruta_2:
        if user == lca:
            break
        camino_bajada.insert(0, user) # Insertar al inicio para invertir el orden

    print (camino_subida + camino_bajada)
    return camino_subida + camino_bajada

# Función para finalizar el trámite
def finalizar_tramite_view(request, pk):
    if request.method == 'POST':
        observacion = request.POST.get('observacion')
        tramite = get_object_or_404(ModelControlTramite, pk=pk)
        try:
            # 2. Actualizar los campos
            tramite.estado_control = True # Marcarlo como inactivo/finalizado
            tramite.estado_ruta_control = True # Marcarlo como inactivo/finalizado
            tramite.fecha_fin_control = datetime.today()
            tramite.instruccion_complementaria_control = observacion
            tramite.save()
            print('ControlTramite modificado')
            try:
                rutas = ModelRutaTramite.objects.filter(Q(control_tramite=tramite) & Q(estado_ruta=False))
                ruta = rutas.first()
                ruta.estado_ruta = True
                ruta.fecha_fin_ruta = datetime.today()
                ruta.destino_nombre_empleado = request.user.get_username()
                ruta.save()
                print('RutaTramite Finalizado')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al finalizar el trámite: {e}')
                return redirect('detailcontrol', pk=pk) # O la URL de donde vino
            
            # Opcional: Notificación
            messages.success(request, f'El Trámite #{tramite.codigo_control} ha sido finalizado exitosamente.')
            # Redirigir a la lista o a otra página
            return redirect('index') 
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error al finalizar el trámite: {e}')
            return redirect('detailcontrol', pk=pk) # O la URL de donde vino
        # Si se accede por GET, redirigir
    return redirect('index')
# Función para crear la primera ruta del trámite
def crear_ruta_tramite_inicial(tramite_id, user, origen, destino, especifica, complementaria):
    """
    Crea y guarda el primer objeto RutaTramite con valores por defecto
    basados en el usuario logueado.
    Args:
        tramite_id (int): El PK del ModelControlTramite padre.
        user (User): El objeto del usuario logueado (request.user).
    Returns:
        RutaTramite: El objeto RutaTramite recién creado.
    """
    
    # 1. Obtener el ModelControlTramite padre
    # Usamos get_object_or_404 para manejar el error si el ID no existe
    control_tramite_obj = get_object_or_404(ModelControlTramite, pk=tramite_id)
    
    # 3. Definir los valores por defecto
    
    # Nota: Los campos deben coincidir con los de tu modelo RutaTramite
    nueva_ruta = ModelRutaTramite(
        # --- Relación ---
        control_tramite=control_tramite_obj, 
        #---- Origen Ruta ---
        origen_ruta = origen,
        # --- Destino ruta ---
        destino_ruta = destino,
        # --- Instruccion complementaria ---
        instruccion_complementaria = complementaria,
        # usuario que la crea
        origen_nombre_empleado = user.get_username()
    )
        # 4. Guardar el objeto en la base de datos
    nueva_ruta.save()
    if especifica:
        # Usamos .set() para añadir las instrucciones seleccionadas al objeto recién guardado.
        nueva_ruta.instruccion_especifica_ruta.set(especifica)
    print(nueva_ruta)
    return nueva_ruta
# Funciona para visualizar en modal el pdf
def servir_pdf_en_linea(request, pk):
    """
    Lee el archivo PDF del ControlTramite y lo sirve con cabeceras que fuerzan
    la visualización en línea (inline).
    """
    # 1. Obtener el objeto para acceder al FileField
    tramite = get_object_or_404(ModelControlTramite, pk=pk)
    print('Trámite para servir PDF:', tramite)
    # 2. Verificar si el archivo existe
    if not tramite.documento_pdf:
        raise Http404("El trámite no tiene un documento adjunto.")

    # 3. Construir la ruta completa del archivo en el sistema de archivos
    # .path devuelve la ruta física del archivo
    file_path = tramite.documento_pdf.path
    
    # 4. Verificar que la ruta sea válida y el archivo exista
    if not os.path.exists(file_path):
        # Aunque el objeto de Django existe, el archivo físico podría no existir.
        raise Http404("El archivo físico no fue encontrado.")

    # 5. Usar FileResponse para servir el archivo
    try:
        # Abre el archivo en modo binario
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        
        # 🌟 CLAVE: Forzar la cabecera Content-Disposition a 'inline' 🌟
        # Esto le dice al navegador que muestre el archivo en lugar de descargarlo
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        
        # Opcional: Agregar cabeceras para prevenir caching agresivo
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    except Exception as e:
        # Manejo de errores al intentar abrir el archivo
        raise Http404(f"Error al servir el archivo: {e}")

def pdf_documento(request, pk):
    """
    Lee el archivo PDF del ControlTramite y lo sirve con cabeceras que fuerzan
    la visualización en línea (inline).
    """
    # 1. Obtener el objeto para acceder al FileField
    documento = get_object_or_404(DocumentoModel, pk=pk)
    print('Documento para servir PDF:', documento)
    # 2. Verificar si el archivo existe
    if not documento.adjunto_documento:
        raise Http404("El documento no tiene un archivo adjunto.")
    # 3. Construir la ruta completa del archivo en el sistema de archivos
    # .path devuelve la ruta física del archivo
    file_path = documento.adjunto_documento.path
    
    # 4. Verificar que la ruta sea válida y el archivo exista
    if not os.path.exists(file_path):
        # Aunque el objeto de Django existe, el archivo físico podría no existir.
        raise Http404("El archivo físico no fue encontrado.")

    # 5. Usar FileResponse para servir el archivo
    try:
        # Abre el archivo en modo binario
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        
        # 🌟 CLAVE: Forzar la cabecera Content-Disposition a 'inline' 🌟
        # Esto le dice al navegador que muestre el archivo en lugar de descargarlo
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        
        # Opcional: Agregar cabeceras para prevenir caching agresivo
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    except Exception as e:
        # Manejo de errores al intentar abrir el archivo
        raise Http404(f"Error al servir el archivo: {e}")

def obtener_ultimo_correlativo(request):
    usuario = UsuarioModel.objects.filter(username_usuario=request.user.username).first()
    acronimo = request.GET.get('acronimo')
    anio_actual = datetime.now().year
    # Supongamos que tu modelo tiene campos 'unidad', 'anio' y 'numero'
    # Buscamos el último documento de esa unidad en el año actual
    ultimo_doc = ModelControlTramite.objects.filter(
        gerencia_codigo_control = usuario.unidad_usuario.acronimo_unidad,
        unidad_destino_codigo_control=acronimo, 
        anio_codigo_control=anio_actual
    ).order_by('-numero_secuencial_codigo_control').first()
    if ultimo_doc:
        nuevo_numero = int(ultimo_doc.numero_secuencial_codigo_control) + 1
    else:
        nuevo_numero = 1 # Si es el primero del año
    # Devolvemos el número formateado (ej: 0001)
    return JsonResponse({'siguiente_numero': str(nuevo_numero).zfill(4)})

def obtener_ultimo_correlativo_documento(request):
    usuario = UsuarioModel.objects.filter(username_usuario=request.user.username).first()
    tipo = request.GET.get('tipo_documento')
    anio_actual = datetime.now().year
    # Supongamos que tu modelo tiene campos 'unidad', 'anio' y 'numero'
    # Buscamos el último documento de esa unidad en el año actual
    ultimo_doc = DocumentoModel.objects.filter(
        tipo_documento = tipo,
        unidad_documento=usuario.unidad_usuario.acronimo_unidad, 
        anio_documento=anio_actual
    ).order_by('-numero_secuencial_documento').first()
    if ultimo_doc:
        nuevo_numero = int(ultimo_doc.numero_secuencial_documento) + 1
    else:
        nuevo_numero = 1 # Si es el primero del año
    # Devolvemos el número formateado (ej: 0001)
    return JsonResponse({'siguiente_numero': str(nuevo_numero).zfill(4)})

# Función para generar PDF
def exportar_pdf(request, pk):
    documento = DocumentoModel.objects.get(pk=pk)
    # Obtener el usuario creador del documento
    user = User.objects.get(pk=documento.usuario_creador_documento.pk)
    # Obtener el objeto UsuarioModel asociado
    usuario = UsuarioModel.objects.filter(username_usuario=user.username).first()
     # plantilla y contexto
    template_path = 'documentos/pdf_template.html'
    context = {'doc': documento, 'usuario': usuario}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{documento}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('Error al generar PDF', status=500)
    return response