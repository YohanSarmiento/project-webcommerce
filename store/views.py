from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages 

def home(request):
    return render(request, 'home.html')

def index(request):
    # Lógica para obtener los productos destacados, ofertas, etc.
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'index.html', {'productos_destacados': productos_destacados})
    
def productos(request):
#    if es_administrador(request.user):
        # Lógica para obtener y mostrar todos los productos disponibles
        # Obtener todos los productos
        productos = Producto.objects.all()
        # Filtrar por nombre
        search_nombre = request.GET.get('search_nombre')
        if search_nombre:
            productos = productos.filter(nombre__icontains=search_nombre)
        # Filtrar por categoría
        search_categoria = request.GET.get('search_categoria')
        if search_categoria:
            productos = productos.filter(categorias__id=search_categoria)
        # Obtener todas las categorías para el formulario de búsqueda
        categorias = Categoria.objects.all()
        return render(request, 'productos.html', {'productos': productos, 'categorias': categorias})
#    else:
#        return HttpResponse("No tienes permiso para ver esta página.")

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

#========================================== Clientes =================================================
def ver_clientes(request):
    clientes = Cliente.objects.filter(es_cliente=True)  # Solo clientes regulares
    return render(request, 'clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirige a la página de lista de clientes
    else:
        form = ClienteForm()
    
    return render(request, 'agregar_cliente.html', {'form': form})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirigir a la lista de clientes después de actualizar
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'actualizar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')  # Redirigir a la lista de clientes después de eliminar
    return redirect('clientes')  # Redirigir a la lista de clientes si no es una solicitud POST

#======================================== Vistas Cliente ============================================
def productos_cliente(request):
    if es_cliente(request.user):
        # Lógica para obtener productos para clientes
        productos = Producto.objects.all()
        return render(request, 'productos_cliente.html', {'productos': productos})
    else:
        return HttpResponse("No tienes permiso para ver esta página.")

def login(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        # Lógica para verificar las credenciales
        # Suponiendo que el correo es único para cada usuario
        try:
            usuario = Cliente.objects.get(correo_electronico=correo, contraseña=contraseña)
            if es_cliente(usuario):
                return redirect('productos_cliente')
            elif es_administrador(usuario):
                return redirect('productos_admin')
            else:
                error_message = "Credenciales incorrectas. Inténtalo de nuevo."
                return render(request, 'login.html', {'error_message': error_message})
        except Cliente.DoesNotExist:
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

#========================================== Comprobacion Usuario =======================================
def es_cliente(usuario):
    # Verifica si el usuario es un cliente
    if hasattr(usuario, 'cliente'):
        return usuario.cliente.es_cliente
    return False

def es_administrador(usuario):
    # Verifica si el usuario es un administrador
    if hasattr(usuario, 'cliente'):
        return usuario.cliente.es_administrador
    return False

#========================================== Proveedores =================================================
def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})

def modificar_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(pk=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'modificar_proveedor.html', {'form': form, 'proveedor': proveedor})

def eliminar_proveedor(request, proveedor_id):
    if request.method == 'POST':
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        proveedor.delete()
        messages.success(request, f'El proveedor "{proveedor.nombre}" ha sido eliminado correctamente.')
        return redirect('proveedores')
    else:
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        return render(request, 'confirmar_eliminar_proveedor.html', {'proveedor': proveedor})