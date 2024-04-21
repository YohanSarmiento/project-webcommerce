from django import forms
from .models import Producto, Proveedor, Categoria

class AgregarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor', 'categorias']

    def __init__(self, *args, **kwargs):
        super(AgregarProductoForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.objects.all()
        self.fields['categorias'].queryset = Categoria.objects.all()

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor', 'categorias']
        
class ModificarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor', 'categorias']