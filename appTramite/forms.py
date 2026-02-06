from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import DocumentoModel, ModelControlTramite, ModelRutaTramite, ModelInstruccionEspecifica
from django.utils import timezone
from datetime import date

class ControlTramiteForm(forms.ModelForm):
    class Meta:
        model = ModelControlTramite
        fields = ['gerencia_codigo_control',
                  'unidad_destino_codigo_control',
                  'anio_codigo_control',
                  'numero_secuencial_codigo_control',
                #   'codigo_control',
                  'asunto_control',
                  'tipo_control',
                  'origen_control', 
                  'nota_control',  
                  'documento_pdf',
                #   'destino_ruta_control',
                #   'instruccion_especifica_control',
                #   'instruccion_complementaria_control'
                ]
        # fields = '__all__' # Incluye todos los campos definidos en el modelo
        
        # Opcional: Personalizar Widgets para una mejor interfaz de usuario
        widgets = {
            # Personalizar el campo booleano a un Checkbox (el default es Select)
            # 'estado_control': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Personalizar el campo de archivo para aceptar solo PDF
            'documento_pdf': forms.FileInput(attrs={'type':'file','accept': '.pdf', 'class': 'form-control'}),
            
            # Opcional: Clases de Bootstrap para otros campos
            'gerencia_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'unidad_destino_codigo_control': forms.Select(attrs={'class': 'form-control', 'title':'Seleccione la unidad destino'}),
            'anio_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'numero_secuencial_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            # 'codigo_control': forms.TextInput(attrs={'class': 'form-control'}),
            'asunto_control': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_control': forms.Select(attrs={'class': 'form-control', 'title':'Seleccione el tipo de documento','required':'required'}),
            'nota_control': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            'origen_control': forms.Select(attrs={'class': 'form-control'}),
            # 'destino_ruta_control':forms.Select(attrs={'class': 'form-control'}),
            # 'instruccion_complementaria_control':forms.TextInput(attrs={'class': 'form-control'}),
        }
        

    def save(self, commit=True):
        """
        Función que sobrescribe el guardado para realizar acciones adicionales,
        como actualizar el estado basado en la fecha_fin.
        """
        instance = super().save(commit=False)

        # Lógica de negocio antes de guardar:
        # Si se introduce una fecha de fin, el trámite pasa a inactivo.
        # if instance.fecha_fin_control and instance.estado_control:
        #     instance.estado_control = False
        
        if commit:
            instance.save()
        return instance

class ControlTramiteDocumentoForm(forms.ModelForm):
    
    class Meta:
        model = ModelControlTramite
        fields = ['gerencia_codigo_control',
                  'unidad_destino_codigo_control',
                  'anio_codigo_control',
                  'numero_secuencial_codigo_control',
                  'asunto_control',
                  'tipo_control',
                  'origen_control', 
                  'nota_control',  # cite del documento origen
                  'documento_pdf',
                  'destino_ruta_control',
                ]
        
        # Opcional: Personalizar Widgets para una mejor interfaz de usuario
        widgets = {
            # Personalizar el campo de archivo para aceptar solo PDF
            'documento_pdf': forms.FileInput(attrs={'type':'file','accept': '.pdf', 'class': 'form-control'}),
            
            # Opcional: Clases de Bootstrap para otros campos
            'gerencia_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'unidad_destino_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'title':'Seleccione la unidad destino', 'readonly':'readonly'}),
            'anio_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'numero_secuencial_codigo_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'asunto_control': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'tipo_control': forms.Select(attrs={'class': 'form-control', 'title':'Seleccione el tipo de documento','readonly':'readonly'}),
            'nota_control': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}), # cite del documento origen
            'origen_control': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'destino_ruta_control':forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),
        }

class RutaTramiteForm(forms.ModelForm):
    instruccion_especifica_ruta = forms.ModelMultipleChoiceField(
        queryset=ModelInstruccionEspecifica.objects.filter(activa_instruccion=True),
        widget=forms.SelectMultiple(
            attrs={
                'id':'selectmultiple',
                'class': 'form-control',  # Clase CSS personalizada
                'multiple': 'multiple'
            }
        ),
        required=False,
        label="Instrucciones especificos",
        # help_text="Puedes seleccionar múltiples instrucciones"
    )
    class Meta:
        model = ModelRutaTramite
        fields = ['usuario_destino_ruta',
                  'documento_adjunto_ruta',
                  'instruccion_especifica_ruta', 
                  'instruccion_complementaria',]
        # Opcional: Personalizar Widgets para una mejor interfaz de usuario
        widgets = {
            'usuario_destino_ruta': forms.Select(attrs={'class':'form-control'}),
            'documento_adjunto_ruta': forms.FileInput(attrs={'type':'file','accept': '.pdf', 'class': 'form-control'}),
            'instruccion_complementaria': forms.TextInput(attrs={'class':'form-control'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoModel
        # Definimos los campos que el usuario podrá llenar manualmente
        # (El cite y usuario_creador se gestionan internamente)
        fields = [
            'titulo_documento',

            'unidad_documento',
            'anio_documento',
            'numero_secuencial_documento',

            'cite_documento', 
            'tipo_documento', 
            'destinatario_documento', 
            'contenido_documento', 
            'adjunto_documento'
        ]
        
        # Etiquetas amigables para el usuario
        labels = {
            'titulo_documento': 'Título del Documento:',
            'cite_documento': 'Cite:',
            'tipo_documento': 'Tipo de Documento:',
            'destinatario_documento': 'Enviar a (Destinatario):',
            # 'contenido_documento': 'Contenido del Documento',
            'adjunto_documento': 'Documento Adjunto (PDF):',
        }

        # Aplicamos widgets para usar clases de CSS (como Bootstrap) y el editor Word
        widgets = {
            'unidad_documento': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'anio_documento': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'numero_secuencial_documento': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),

            'titulo_documento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Escriba un título descriptivo...'
            }),
            'cite_documento': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'destinatario_documento': forms.Select(attrs={'class': 'form-control'}),
            'contenido_documento': CKEditorWidget(config_name='default', attrs={'class': 'form-control'}), # El editor tipo Word
            'adjunto_documento': forms.FileInput(attrs={'type':'file','accept': '.pdf', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        # Opcional: Podrías filtrar aquí los destinatarios para que no aparezca el propio usuario
        # self.fields['destinatario'].queryset = User.objects.exclude(id=user_id)