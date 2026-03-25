from django.contrib import admin
from .models import Usuario,Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display=("id","nome","cnpj")
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display=("id","username","email","empresa","is_staff")
    list_filter=("empresa","is_staff")