from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages 
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import csv
from itertools import groupby
from django.forms.models import model_to_dict

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
        form = ProductoForm(request.POST, request.FILES)  # Agrega request.FILES para manejar imágenes
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado con éxito!')
            return redirect('productos')
    else:
        form = ProductoForm()
    
    proveedores = Proveedor.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'add_producto.html', {'form': form, 'proveedores': proveedores, 'categorias': categorias})

def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    proveedores = Proveedor.objects.all()
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        form = ModificarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto_modificado = form.save(commit=False)
            # Crear una copia del producto antes de guardar los cambios
            producto_anterior = model_to_dict(producto)
            # Verificar si se ha subido una nueva imagen
            if 'imagen' in request.FILES:
                producto_modificado.imagen = request.FILES['imagen']
            producto_modificado.save()
            # Comparar los valores anteriores con los nuevos valores
            cambios = []
            for campo, valor_anterior in producto_anterior.items():
                valor_nuevo = getattr(producto_modificado, campo)
                if valor_anterior != valor_nuevo:
                    cambios.append(f"{campo}: {valor_anterior} -> {valor_nuevo}")
            # Guardar el historial de cambios
            HistorialCambioProducto.objects.create(
                producto=producto_modificado,
                usuario=request.user,
                campo_modificado='Modificación de Producto',
                valor_anterior='\n'.join(cambios) if cambios else 'Sin cambios',
                valor_nuevo='Detalles del producto después de la modificación'
            )
            return redirect('detalle_producto', producto_id=producto_id)
    else:
        form = ModificarProductoForm(instance=producto)

    return render(request, 'modificar_producto.html', {'form': form, 'producto': producto, 'proveedores': proveedores, 'categorias': categorias})

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
    
# ========================================== Inventario =============================================
def invetario(request):
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
    return render(request, 'invetario.html', {'productos': productos, 'categorias': categorias})

def generar_reporte_inventario(request):
    # Obtener el formato deseado del reporte (pdf, csv o txt)
    formato = request.GET.get('formato', 'pdf')
    # Obtener todos los productos
    productos = Producto.objects.all()
    if formato == 'pdf':
        # Generar el reporte en formato PDF
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        data = [['Nombre', 'Precio', 'Stock', 'Proveedor']]
        for producto in productos:
            data.append([producto.nombre, producto.precio, producto.stock, producto.proveedor])
        tabla = Table(data)
        estilo = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                             ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        tabla.setStyle(estilo)
        elementos = [tabla]
        pdf.build(elementos)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
        response.write(buffer.getvalue())
        buffer.close()
        return response
    elif formato == 'csv':
        # Generar el reporte en formato CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Precio', 'Stock', 'Proveedor'])
        for producto in productos:
            writer.writerow([producto.nombre, producto.precio, producto.stock, producto.proveedor])
        return response
    elif formato == 'txt':
        # Generar el reporte en formato texto plano
        contenido_reporte = "Reporte de Inventario:\n\n"
        for producto in productos:
            contenido_reporte += f"Nombre: {producto.nombre}\n"
            contenido_reporte += f"Precio: {producto.precio}\n"
            contenido_reporte += f"Stock: {producto.stock}\n"
            contenido_reporte += f"Proveedor: {producto.proveedor}\n"
            contenido_reporte += "--------------------------\n"
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.txt"'
        response.write(contenido_reporte)
        return response
    else:
        # Manejar un formato no válido
        return HttpResponse("Formato de reporte no válido.")
    
def historial_cambios(request):
    historial = HistorialCambioProducto.objects.all().order_by('-fecha_cambio')
    cambios_agrupados = []
    
    # Agrupar los cambios por producto
    for key, group in groupby(historial, lambda x: x.producto):
        cambios_agrupados.append(list(group))

    return render(request, 'historial_cambios.html', {'cambios_agrupados': cambios_agrupados})

def eliminar_historial(request):
    if request.method == 'POST':
        # Eliminar todos los registros del historial de cambios
        HistorialCambioProducto.objects.all().delete()
        # Redireccionar a la página de inicio o a otra página de confirmación
        return redirect('historial_cambios')  # Cambia 'inicio' por la URL a la que deseas redirigir
    
    # Si no es una solicitud POST, simplemente redirecciona a alguna página, como la de inicio
    return redirect('historial_cambios')  # Cambia 'inicio' por la URL a la que deseas redirigir

def lista_reabastecimientos(request):
    reabastecimientos = Reabastecimiento.objects.all().order_by('-fecha')
    return render(request, 'lista_reabastecimientos.html', {'reabastecimientos': reabastecimientos})

def reabastecer_productos(request):
    if request.method == 'POST':
        productos_bajo_stock = Producto.objects.filter(stock__lt=10)
        for producto in productos_bajo_stock:
            cantidad_reabastecida = 10  # Ajusta el valor según tus necesidades

            # Registrar el pedido de reabastecimiento sin modificar el stock
            Reabastecimiento.objects.create(
                producto=producto,
                cantidad=cantidad_reabastecida,
                usuario=request.user
            )

        #messages.success(request, 'Pedidos de reabastecimiento registrados. Confirme los pedidos para actualizar el stock.')
        return redirect('inventario')  # Cambia 'tu_vista_de_inventario' por el nombre de tu vista de inventario

def confirmar_reabastecimiento(request, reabastecimiento_id):
    reabastecimiento = get_object_or_404(Reabastecimiento, pk=reabastecimiento_id)
    if reabastecimiento.estado == 'pendiente':
        producto = reabastecimiento.producto
        producto.stock += reabastecimiento.cantidad
        producto.save()
        reabastecimiento.estado = 'confirmado'
        reabastecimiento.save()
        messages.success(request, 'Reabastecimiento confirmado y stock actualizado.')
    return redirect('lista_reabastecimientos')