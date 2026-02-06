from django.contrib import admin
from .models import UnidadModel, UsuarioModel

# Register your models here.
# class GrupoAdmin(admin.ModelAdmin):
#     filter_horizontal = ("usuarios",)
# class UsuarioAdmin(admin.ModelAdmin):
#     filter_horizontal = ("unidad_usuario",)

admin.site.register(UnidadModel)
admin.site.register(UsuarioModel) 