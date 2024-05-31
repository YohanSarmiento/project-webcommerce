from django import forms
from .models import Producto, Proveedor, Categoria, Cliente
from django.contrib.auth.forms import AuthenticationForm

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
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'correo_electronico', 'contraseña']
        
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'correo_electronico']
        
        
#====================================== Separacion de inicio de sesion ========================================     
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo Electrónico'
