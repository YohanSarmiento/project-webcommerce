from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "description")

admin.site.register(Customer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)