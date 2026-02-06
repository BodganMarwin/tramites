from django.contrib import admin
from .models import ModelControlTramite,ModelRutaTramite, ModelInstruccionEspecifica, DocumentoModel

# Register your models here.

admin.site.register(ModelControlTramite)
admin.site.register(ModelRutaTramite)
admin.site.register(ModelInstruccionEspecifica)
admin.site.register(DocumentoModel)