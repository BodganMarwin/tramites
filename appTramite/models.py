from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import Group,User
from django.utils import timezone
from datetime import datetime
from appAuth.models import UsuarioModel, UnidadModel

# Create your models here.

# OPCIONES_GERENCIA_UNIDAD (ACTUALIZADO CON TODAS LAS IMÁGENES)
def get_group_choices():
    group_choices = []
    # Obtiene todos los grupos de la base de datos
    for group in UnidadModel.objects.all():
        # Agrega una tupla (id_del_grupo, nombre_del_grupo) a la lista
        group_choices.append((group.id, group.name))
    return group_choices
OPCIONES_GERENCIA_UNIDAD = (
    ('GERENCIA GENERAL', 'Gerencia General'),
    ('ASESORIA LEGAL', 'Asesoría Legal'),
    ('CLUB GENTE GRANDE', 'Club Gente Grande'),
    ('AMBITO REGULATORIO', 'Ámbito Regulatorio'),
    ('DIVISION TECNOLOGIAS DE LA INFORMACION', 'Tecnologías de la Información'),
    ('GERENCIA COMERCIAL', 'Gerencia Comercial'),
    ('GERENCIA COMERCIAL CORPORATIVA', 'Gerencia Comercial Corporativa'),
    ('EQUIPO VENTAS EMPRESAS', 'Equipo Ventas Empresas'),
    ('EQUIPO DESARROLLO MARKETING COMUNICACION', 'Equipo Desarrollo de Marketing y Comunicación'),
    ('EQUIPO TRABAJO TERRITORIO SUD', 'Equipo de Trabajo Territorio Sud'),
    ('EQUIPO TRABAJO TERRITORIO QUILLACOLLO', 'Equipo de Trabajo Territorio Quillacollo'),
    ('EQUIPO TRABAJO TERRITORIO NORTE', 'Equipo de Trabajo Territorio Norte'),
    ('EQUIPO TRABAJO TERRITORIO HIPODROMO', 'Equipo de Trabajo Territorio Hipódromo'),
    ('EQUIPO TRABAJO TERRITORIO CENTRO', 'Equipo de Trabajo Territorio Centro'),
    ('EQUIPO CENTRO DE LLAMADAS', 'Equipo Centro de Llamadas'),
    ('EQUIPO ATENCION RETENCION SOCIO', 'Equipo Atención y Retención al Socio'),
    ('EQUIPO ATENCION RETENCION CLIENTE', 'Equipo Atención y Retención al Cliente'),
    ('DIVISION RELACION EXPERIENCIA CLIENTE', 'División Relación y Experiencia del Cliente'),
    ('DIVISION GESTION INTEGRAL TERRITORIOS', 'División Gestión Integral de Territorios'),
    ('DIVISION GESTION DE LA OFERTA', 'División Gestión de la Oferta'),
    ('GERENCIA ADMINISTRACION FINANZAS', 'Gerencia de Administración y Finanzas'),
    ('DEPARTAMENTO CONTABILIDAD', 'Departamento Contabilidad'),
    ('DIVISION FACTURACION COBRANZAS', 'División Facturación y Cobranzas'),
    ('DIVISION FINANZAS', 'División Finanzas'),
    ('UNIDAD ATENCION RECLAMOS FACTURA', 'Unidad de Trabajo Atención Reclamos Factura'),
    ('UNIDAD TRABAJO CARTERA', 'Unidad de Trabajo Cartera'),
    ('UNIDAD TRABAJO COBRANZAS', 'Unidad de Trabajo Cobranzas'),
    ('UNIDAD TRABAJO PROCESOS', 'Unidad de Trabajo Procesos'),
    ('DEPARTAMENTO ACTIVOS FIJOS', 'Departamento Activos Fijos'),
    ('DEPARTAMENTO EXTENSION SOCIAL COOPERATIVA', 'Departamento Extensión Social Cooperativa'),
    ('DIVISION ADMINISTRACION SERVICIOS', 'División Administración y Servicios'),
    ('DIVISION GESTION DE RECURSOS HUMANOS', 'División Gestión de Recursos Humanos'),
    ('GERENCIA ADMINISTRACION ABASTECIMIENTO', 'Gerencia de Administración de Abastecimiento'),
    ('UNIDAD TRABAJO ALMACENES', 'Unidad de Trabajo Almacenes'),
    ('UNIDAD TRABAJO ARCHIVOS', 'Unidad de Trabajo Archivos'),
    ('UNIDAD TRABAJO SEGURIDAD FISICA INDUSTRIAL', 'Unidad de Trabajo Seguridad Física e Industrial'),
    ('UNIDAD TRABAJO SEGURO DELEGADO', 'Unidad de Trabajo Seguro Delegado'),
    ('UNIDAD TRABAJO SERVICIOS GENERALES LOGISTICA', 'Unidad de Trabajo Servicios Generales y Logística'),
    ('UNIDAD TRABAJO TALLERES', 'Unidad de Trabajo Talleres'),
    ('GERENCIA PRODUCCION', 'Gerencia Produccion'),
    ('CENTRO OPERACIONES CENTRO CONDEBAMBA', 'Centro de Operaciones Centro Condebamba'),
    ('CENTRO OPERACIONES HIPODROMO', 'Centro de Operaciones Hipódromo'),
    ('CENTRO OPERACIONES NORTE SACABA', 'Centro de Operaciones Norte Sacaba'),
    ('CENTRO OPERACIONES QUILLACOLLO', 'Centro de Operaciones Quillacollo'),
    ('CENTRO OPERACIONES SUD VALLE', 'Centro de Operaciones Sud Valle'),
    ('DEPARTAMENTO DWDM', 'Departamento DWDM'),
    ('DEPARTAMENTO ENERGIA FUERZA', 'Departamento Energía y Fuerza'),
    ('DEPARTAMENTO INTERNET', 'Departamento Internet'),
    ('DEPARTAMENTO PLATAFORMAS TRANSMISION TERRESTRE', 'Departamento Plataformas de Transmisión Terrestre'),
    ('DEPARTAMENTO TELEVISION', 'Departamento Televisión'),
    ('DEPARTAMENTO TRANSPORTE INALAMBRICO', 'Departamento Transporte Inalámbrico'),
    ('DEPARTAMENTO VOZ', 'Departamento Voz'),
    ('DIVISION GESTION DE RECURSOS PRODUCCION', 'División Gestión de Recursos'),
    ('DIVISION GESTION DEL SERVICIO', 'División Gestión del Servicio'),
    ('HELP DESK', 'Help Desk'),
    ('APLICACIONES', 'Aplicaciones'),
    ('GESTION INVENTARIO RECURSOS', 'Gestión del Inventario de Recursos'),
    ('MONITOREO SERVICIOS RECURSOS', 'Monitoreo Servicios y Recursos'),
    ('MANTENIMIENTO DE REDES', 'Mantenimiento de Redes'),
    ('MESA DE PRUEBAS', 'Mesa de Pruebas'),
    ('GERENCIA PLANIFICACION', 'Gerencia de Planificación'),
    ('DIVISION PLANIFICACION DISENO REDES', 'División Planificación y Diseño de Redes'),
    ('DIVISION PLANIFICACION CONTROL GESTION', 'División Planificación y Control de Gestión'),
    ('DIVISION GESTION DE CALIDAD', 'División Gestión de Calidad'))
TIPO = (('NOTA','Nota'),('INFORME','Informe'),('COMUNICADO_INTERNO','Comunicado Interno'))
TIPO_CHOICES = [
        ('C', 'Carta'),
        ('N', 'Nota Interna'),
        ('INF', 'Informe'),
        ('CIR', 'Circular'),
        ('M', 'Memorandum'),
    ]
abecedario = [('A', 'A'),
              ('B', 'B'),
              ('C', 'C'),
              ('D', 'D'),
              ('E', 'E'),
              ('F', 'F'),
              ('G', 'G'),
              ('H', 'H'),
              ('I', 'I'),
              ('J', 'J'),
              ('K', 'K'),
              ('L', 'L'),
              ('M', 'M'),
              ('N', 'N'),
              ('O', 'O'),
              ('P', 'P'),
              ('Q', 'Q'),
              ('R', 'R'),
              ('S', 'S'),
              ('T', 'T'),
              ('U', 'U'),
              ('V', 'V'),
              ('W', 'W'),
              ('X', 'X'),
              ('Y', 'Y'),
              ('Z', 'Z')]
# def get_unidad_choices():
#     unidad_choices = []
#     for unidad in UnidadModel.objects.all():
#         unidad_choices.append((unidad.acronimo_unidad, unidad.nombre_unidad))
#     unidad_choices += abecedario
#     return unidad_choices


def get_unidad_choices():
    unidad_choices = []
    try:
        # Intentamos obtener los datos de la base de datos
        for unidad in UnidadModel.objects.all():
            unidad_choices.append((unidad.acronimo_unidad, unidad.nombre_unidad))
    except:
        # Si la tabla no existe (en migraciones iniciales), ignoramos el error
        pass
        
    unidad_choices += abecedario
    return unidad_choices

UNIDAD_CHOICES = get_unidad_choices
TIPO_RUTA = [
    ('CONTROL','Control'),
    ('REVISION','Revision'),
    ('OTRO','Otro'),
]
################################################################################################################
# clase INSTRUCCION ESPECIFICA
################################################################################################################
class ModelInstruccionEspecifica(models.Model):
    """Modelo para categorías de trámites"""
    titulo_instruccion= models.CharField(max_length=100, unique=True)
    descripcion_instruccion = models.TextField(blank=True)
    activa_instruccion = models.BooleanField(default=True)
    fecha_instruccion = models.DateField(verbose_name="Fecha", auto_now_add=True)
    
    class Meta:
        db_table = 'instruccionespecifica'
        verbose_name = "Instrucción Especifica"
        verbose_name_plural = "Instrucciones Especificas"
        # ordering = ['titulo_instruccion']
    
    def __str__(self):
        return self.titulo_instruccion
################################################################################################################
# clase ControlTramite
################################################################################################################
class ModelControlTramite(models.Model):
   
    fecha_ini_control = models.DateTimeField(verbose_name="Fecha", auto_now_add=True)
    fecha_fin_control = models.DateTimeField(verbose_name="Fecha Fin Control",null=True, blank=True)

    # Código de Control desglosado
    gerencia_codigo_control = models.CharField(max_length=150, verbose_name="Gerencia/Unidad Responsable", blank=True) # Unidad de donde se crea el control de tramite
    unidad_destino_codigo_control = models.CharField(max_length=150, verbose_name="Unidad Origen del Doc.", choices=UNIDAD_CHOICES,blank=True,) # Unidad de origen del documento
    anio_codigo_control = models.CharField(max_length=4, verbose_name="Año de Trámite", blank=True)
    numero_secuencial_codigo_control = models.CharField(max_length=20, verbose_name="Número Secuencial", blank=True)
    # código de control completo (STRING)
    codigo_control = models.CharField(max_length=50, verbose_name="Código de Control",unique=True)
    
    # Asunto del control de tramite
    asunto_control = models.CharField(max_length=255,verbose_name="Asunto del Trámite" )
    # tipo de documento del control de tramite
    tipo_control = models.CharField( max_length=100, verbose_name="Tipo Documento", choices=TIPO_CHOICES, blank=True, null=True)
    # estado del control de tramite
    estado_control = models.BooleanField(verbose_name="Estado Activo/Inactivo", null=True,blank=True, default=False )
    
    # --- Origen y Destino ---
    
    LISTA_TEMPORAL = list(OPCIONES_GERENCIA_UNIDAD)
    agregar = ("NOTA_EXTERNO","Nota Externa")
    LISTA_TEMPORAL.append(agregar)
    OPCIONES = tuple(LISTA_TEMPORAL)

    # origen_control de donde salio el documento generador del control del tramite (STRING)
    origen_control = models.CharField(max_length=150, verbose_name="Unidad Origen del Trámite", choices=OPCIONES )
    # cite del documento del control de tramites (STRING)
    nota_control = models.CharField(max_length=100,verbose_name="Nota de Control", blank=True)
    # atributos adicionales q no se usan por ahora
    informe_control = models.CharField(verbose_name="Informe de Control",blank=True)
    com_int_control = models.CharField(verbose_name="ComInt",blank=True)

    # documento pdf (FILE)
    documento_pdf = models.FileField(upload_to='documentosTramites/%Y/%m/%d/', verbose_name="Documento Adjunto (PDF)",validators=[FileExtensionValidator(allowed_extensions=['pdf'])]) 
    # usuario empleado responsable (FOREIGN KEY) q creo el tramite
    nombre_empleado_control = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Empleado Responsable", blank=True, null=True)
    ########################################################
    # atributos del tramite q son parte de la ruta
    # origen ruta control (STRING)
    origen_ruta_control = models.CharField(max_length=150, verbose_name="Unidad Origen", blank=True)
    # destino de ruta (STRING) donde se enviará el tramite lo utilziamos para mostrar en los tramites pendientes del usuario
    destino_ruta_control = models.ForeignKey(UnidadModel,on_delete=models.RESTRICT,verbose_name="Unidad Destino del Tramite", blank=True,null=True)
    # usuario destino de la ruta, donde se enviara el tramite 
    usuario_ruta_control = models.ForeignKey(UsuarioModel, on_delete=models.RESTRICT, verbose_name="Usuario Jerarquico Responsable", blank=True, null=True,related_name="usuario_destino")
    #
    destino_jerarquia_control = models.ForeignKey(UnidadModel,on_delete=models.RESTRICT,verbose_name="Destino Jerarquico del Tramite", blank=True,null=True, related_name="tramites_jerarquia")
    usuario_jerarquia_control = models.ForeignKey(UsuarioModel, on_delete=models.RESTRICT, verbose_name="Usuario Jerarquico Responsable", blank=True, null=True, related_name="usuario_jerarquia")
    # crea el path momentaneo del usuario_a al usuario_b
    path_jerarquia_control = models.TextField(verbose_name="Path de usuario_a al usuario_b", blank=True)
    

    # Instruccion especifica puede seleccionar una o varias opciones (STRING)
    instruccion_especifica_control=models.ManyToManyField( ModelInstruccionEspecifica,verbose_name="Intrucción Especifica",blank=True, help_text="Selecciona una o más categorías" )
    # Instruccion Complementaria (STRING)
    instruccion_complementaria_control=models.TextField(verbose_name="Instrucción Complementaria", blank=True)
    # Estado de la ruta inicial
    estado_ruta_control = models.BooleanField(verbose_name="Estado derivación inicial",default=False,blank=True, null=True)



    # --- Metadatos de Django ---
    class Meta:
        db_table = "controltramite"
        verbose_name = "Control de Trámite"
        verbose_name_plural = "Controles de Trámites"
        # Puedes añadir ordering = ['-fecha_ini_control'] para ordenar por defecto

    def __str__(self):
        return f"{self.codigo_control} - {self.asunto_control}"
    def get_tipo_control_display(self):
        return dict(TIPO_CHOICES).get(self.tipo_control, 'Desconocido')


################################################################################################################
# clase rutatramite
################################################################################################################

class ModelRutaTramite(models.Model):
    """
    Modelo que registra el movimiento de un trámite. 
    Es dependiente de ControlTramite.
    """
    # Esta línea establece la dependencia.
    control_tramite = models.ForeignKey('ModelControlTramite',on_delete=models.RESTRICT,  related_name='rutas_asociadas', verbose_name="Trámite")
    # origenruta (STRING)
    origen_ruta = models.CharField(max_length=150, verbose_name="Origen de la Ruta")
    # destinoruta (STRING)
    destino_ruta = models.ForeignKey(UnidadModel, on_delete=models.RESTRICT, verbose_name="Destino de la Ruta",)
    # Usuario destinatario
    usuario_destino_ruta = models.ForeignKey(UsuarioModel,on_delete=models.RESTRICT, verbose_name="Destinatario", blank=True, null=True)
    # fechainiruta (DATE ONLY)
    fecha_ini_ruta = models.DateTimeField(verbose_name="Fecha Inicio de Ruta",auto_now_add=True)
    # fechafinruta (DATE ONLY)
    fecha_fin_ruta = models.DateTimeField(verbose_name="Fecha Fin de Ruta",null=True, blank=True)
    # fecharesepcionruta (DATE ONLY)
    fecha_resepcion_ruta = models.DateTimeField(verbose_name="Fecha de Recepción de Ruta", null=True,blank=True )
    # estadoruta (BOOLEAN)
    estado_ruta = models.BooleanField(verbose_name="Ruta Activa",null=True,blank=True,default=False )
    # documentoadjuntoruta (FILE)
    documento_adjunto_ruta = models.FileField(upload_to='documentosRutas/%Y/%m/%d/', verbose_name="Documento Adjunto de la Ruta (PDF)",validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    # tipo de ruta 
    tipo_ruta = models.CharField(max_length=150, verbose_name="Tipo de Ruta",choices=TIPO_RUTA, blank=True, null=True)

    # instruccionespecifica (STRING)
    instruccion_especifica = models.TextField(max_length=150,verbose_name="Instrucción Específica",blank=True, )
    instruccion_especifica_ruta = models.ManyToManyField(ModelInstruccionEspecifica,verbose_name="Instrucción Específica",blank=True, help_text="Selecciona una o más categorías")
    


    # instrucciones Especificas
    ie_para_su_atencion = models.BooleanField(verbose_name="1. Para su Atención", null=True, blank=True,)
    ie_para_su_conocimiento = models.BooleanField(verbose_name="2. Para su Conocimiento",null=True,blank=True,)
    ie_para_su_analsis = models.BooleanField(verbose_name="3. Para su Análisis e Informe", null=True,blank=True,)
    ie_para_su_aprobacion = models.BooleanField(verbose_name="4. Para su Aprobación", null=True, blank=True,)
    ie_para_su_regularizacion = models.BooleanField(verbose_name="5. Para su Regularización",null=True,blank=True,)
    ie_proceder_al_pago = models.BooleanField(verbose_name="6. Proceder al Pago",null=True,blank=True,)
    ie_para_su_archivo = models.BooleanField(verbose_name="7. Para su Archivo",null=True,blank=True,)
    ie_dar_cumplimiento = models.BooleanField(verbose_name="8. Dar Cumplimiento", null=True,blank=True,)
    ie_tratamiento_urgente = models.BooleanField(verbose_name="9. Tratamiento Urgente",null=True,blank=True,)
    ie_se_adjunta_nota = models.BooleanField(verbose_name="10. Se Adjunta Nota", null=True, blank=True,)
    ie_para_descargo = models.BooleanField(verbose_name="11. Para Descargo", null=True,blank=True,)
    ie_autorizado = models.BooleanField(verbose_name="12. Autorizado", null=True,blank=True,)
    ie_elaborar_contrato = models.BooleanField(verbose_name="13. Elaborar Contrato",null=True,blank=True,)
    ie_otro = models.BooleanField(verbose_name="14. Otros",null=True,blank=True,)


    # instruccion complementaria (STRING)
    instruccion_complementaria = models.TextField(verbose_name="Instrucción Complementaria",blank=True)
    # origennombreempleado (STRING)
    origen_nombre_empleado = models.CharField( max_length=200,verbose_name="Nombre Empleado Origen")

    # destinonombreempleado (STRING)
    destino_nombre_empleado = models.CharField(max_length=200,verbose_name="Nombre Empleado Destino",blank=True,null=True)
    
    # --- Metadatos ---
    class Meta:
        db_table = "rutatramite" 
        verbose_name = "Ruta de Trámite"
        verbose_name_plural = "Rutas de Trámites"

    def __str__(self):
        return f"Ruta {self.id} | Trámite: {self.control_tramite} | {self.origen_ruta} -> {self.destino_ruta}"
    
################################################################################################################
# clase documento
################################################################################################################

class DocumentoModel(models.Model):
    

    # Código de Control desglosado
    unidad_documento = models.CharField(max_length=150, verbose_name="Unidad Origen", choices=UNIDAD_CHOICES,blank=True,)
    anio_documento = models.CharField(max_length=4, verbose_name="Año de Documento", blank=True)
    numero_secuencial_documento = models.CharField(max_length=20, verbose_name="Número Secuencial", blank=True)

    # Atributos del Documento
    cite_documento = models.CharField(max_length=50, unique=True, verbose_name="Cite", blank=True)
    fecha_documento = models.DateField(auto_now_add=True)
    titulo_documento = models.CharField(max_length=255)
    contenido_documento = RichTextField()  # El editor tipo Word
    tipo_documento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    adjunto_documento = models.FileField(upload_to='media/CNITM/%Y/%m/', null=True, blank=True)
    
    # Relaciones
    usuario_creador_documento = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='creador')
    destinatario_documento = models.ForeignKey(UsuarioModel, on_delete=models.RESTRICT, related_name='destinatario')
    bpm_control_documento = models.ForeignKey(ModelControlTramite, on_delete=models.SET_NULL, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.cite_documento:
    #         # Lógica de Cite: dti-2026-0001
    #         anio = datetime.now().year
    #         # Asumimos que el usuario tiene un perfil con la sigla de su unidad
    #         usuario = UsuarioModel.objects.get(pk=self.usuario_creador_documento.pk)
    #         unidad = usuario.unidad_usuario.acronimo_unidad # Esto podría venir de self.usuario_creador_documento.profile.unidad
            
    #         ultimo_doc = DocumentoModel.objects.filter(
    #             cite_documento__contains=f"{unidad}-{anio}"
    #         ).order_by('-id').first()

    #         if ultimo_doc:
    #             # Extraer el número del cite ej: dti-2026-0001 -> 0001
    #             ultimo_numero = int(ultimo_doc.cite_documento.split('-')[-1])
    #             nuevo_numero = ultimo_numero + 1
    #         else:
    #             nuevo_numero = 1

    #         self.cite_documento = f"{unidad}-{anio}-{nuevo_numero:04d}"
        
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cite_documento} - {self.titulo_documento}"
    
    class Meta:
        db_table = 'documento'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'