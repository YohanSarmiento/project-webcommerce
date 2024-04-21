from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),  # Listado de productos
    path('add_producto/', views.add_producto, name='add_producto'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),  # Detalle de un producto específico
    path('producto/<int:producto_id>/modificar/', views.modificar_producto, name='modificar_producto'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)