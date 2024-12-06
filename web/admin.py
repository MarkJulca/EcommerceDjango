from django.contrib import admin

# Register your models here.
from .models import Categoria,Producto

admin.site.register(Categoria)
#admin.site.register(Producto)
# "decorador" para agregar funciones especiales se hace asi
#list_display es para poner lo que queremos que se muestre en listado
#list_editable de los campos en display ponemos que el precio sea editable
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio','categoria','fecha_registro')
    list_editable = ('precio',)