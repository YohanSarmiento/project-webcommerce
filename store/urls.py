from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.view_products, name='view_products'),
    path('get-products-by-category/<int:category_id>/', views.get_products_by_category, name='get_products_by_category'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)