from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Producto, Proveedor, Categoria
from .forms import AgregarProductoForm, ModificarProductoForm
from django.contrib import messages 

def home(request):
    return render(request, 'home.html')

def index(request):
    # Lógica para obtener los productos destacados, ofertas, etc.
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'index.html', {'productos_destacados': productos_destacados})

def productos(request):
    # Lógica para obtener y mostrar todos los productos disponibles
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

#def add_producto(request):
#    # Lógica para obtener y mostrar todos los productos disponibles
#    return render(request, 'add_producto.html')

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def add_producto(request):
    if request.method == 'POST':
        form = AgregarProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado con éxito!')
            # Redireccionar a la misma página después de guardar el producto
            return redirect('add_producto')
    else:
        form = AgregarProductoForm()
    
    # Obtener todos los proveedores y categorías
    proveedores = Proveedor.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'add_producto.html', {'form': form, 'proveedores': proveedores, 'categorias': categorias})

def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ModificarProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Puedes agregar un mensaje de éxito aquí si lo deseas
            return redirect('detalle_producto', producto_id=producto_id)
    else:
        form = ModificarProductoForm(instance=producto)
    
    return render(request, 'modificar_producto.html', {'form': form})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        # Puedes agregar un mensaje de éxito aquí si lo deseas
        return redirect('productos')
    
    return render(request, 'confirmar_eliminar_producto.html', {'producto': producto})