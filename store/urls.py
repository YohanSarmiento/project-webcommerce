from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    # path('', views.home, name='login'),
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
    path('proveedores/', views.proveedores, name='proveedores'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedor/<int:proveedor_id>/modificar', views.modificar_proveedor, name='modificar_proveedor'),
    path('proveedor/<int:proveedor_id>/eliminar', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('invetario/', views.invetario, name='inventario'),  # Listado de INVENTARIO
    path('generar_reporte_inventario/', views.generar_reporte_inventario, name='generar_reporte_inventario'),
    path('historial-cambios/', views.historial_cambios, name='historial_cambios'),
    path('eliminar-historial/', eliminar_historial, name='eliminar_historial'),
    
    path('reabastecer-productos/', views.reabastecer_productos, name='reabastecer_productos'),
    path('reabastecer-producto/<int:producto_id>/', views.reabastecer_producto, name='reabastecer_producto'),
    path('lista-reabastecimientos/', views.lista_reabastecimientos, name='lista_reabastecimientos'),
    path('cancelar-reabastecimiento/<int:reabastecimiento_id>/', views.cancelar_reabastecimiento, name='cancelar_reabastecimiento'),
    path('confirmar-reabastecimiento/<int:reabastecimiento_id>/', views.confirmar_reabastecimiento, name='confirmar_reabastecimiento'),
    
    
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.compras_cliente, name='compras_cliente'),
    
    path('realizar_venta/<int:producto_id>/', views.realizar_venta, name='realizar_venta'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    
    path('generar_reporte_ventas/csv/', views.generar_reporte_ventas_csv, name='generar_reporte_ventas_csv'),
    path('generar_reporte_ventas/pdf/', views.generar_reporte_ventas_pdf, name='generar_reporte_ventas_pdf'),
    
    path('eliminar_ventas/', views.eliminar_ventas, name='eliminar_ventas'),
    path('eliminar_reabastecimiento/', views.eliminar_reabastecimiento, name='eliminar_reabastecimiento'),

  

    path('home_cliente/', views.home_cliente, name='home_cliente'),
    path('products/', views.view_products, name='view_products'),
    path('get-products-by-category/<int:category_id>/', views.get_products_by_category, name='get_products_by_category'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)