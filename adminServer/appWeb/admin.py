from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario


class ServidorResource(resources.ModelResource):
    class Meta:
        model = Servidor


class UsuarioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ["usr"]
    list_display = ("usr","pwd","nombres","apellidos","correo","numero","chat_id","token")
    resource_class = UsuarioResource


class ServidorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ["id","desc_srv"]
    list_display = ("id","desc_srv","ip_srv","puerto","usr")
    resource_class = ServidorResource


# Register your models here.
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Servidor,ServidorAdmin)
