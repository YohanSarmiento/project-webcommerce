from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='login'),
    path('productos/', views.productos, name='productos'),  # Listado de productos
    path('add_producto/', views.add_producto, name='add_producto'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),  # Detalle de un producto específico
    path('producto/<int:producto_id>/modificar/', views.modificar_producto, name='modificar_producto'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('clientes/', views.ver_clientes, name='clientes'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/<int:cliente_id>/modificar/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
#    path('productos/cliente/', views.productos_cliente, name='productos_cliente'),  # Página de productos para clientes
    path('proveedores/', views.proveedores, name='proveedores'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedor/<int:proveedor_id>/modificar', views.modificar_proveedor, name='modificar_proveedor'),
    path('proveedor/<int:proveedor_id>/eliminar', views.eliminar_proveedor, name='eliminar_proveedor'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)