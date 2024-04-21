from django.contrib import admin
from .models import Proveedor, Categoria, Producto, Cliente, Pedido, DetallePedido
from .forms import ProductoForm

# Register your models here.


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'correo_electronico')
    search_fields = ('nombre', 'direccion', 'telefono', 'correo_electronico')

admin.site.register(Proveedor, ProveedorAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Categoria, CategoriaAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'stock', 'proveedor')
    list_filter = ('proveedor', 'categorias')
    search_fields = ('nombre', 'descripcion')
    
    form = ProductoForm  # Aquí vinculamos el formulario personalizado

    def categorias(self, obj):
        return ", ".join([c.nombre for c in obj.categorias.all()])

admin.site.register(Producto, ProductoAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'direccion', 'telefono', 'correo_electronico')
    search_fields = ('nombre', 'apellido', 'direccion', 'telefono', 'correo_electronico')

admin.site.register(Cliente, ClienteAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_pedido', 'estado_pedido')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'estado_pedido')

admin.site.register(Pedido, PedidoAdmin)

class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__cliente__nombre', 'pedido__cliente__apellido', 'producto__nombre')

admin.site.register(DetallePedido, DetallePedidoAdmin)