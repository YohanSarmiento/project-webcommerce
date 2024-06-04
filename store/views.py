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
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas

from django.http import JsonResponse
from django.shortcuts import redirect
from decimal import Decimal


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
    # Lógica para obtener productos para clientes
    productos = Producto.objects.all()
    return render(request, 'productos_cliente.html', {'productos': productos})

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
            form.save()  # Guardar el formulario creará y guardará un nuevo Proveedor en la base de datos
            return redirect('proveedores')  # Redirigir a la página de proveedores después de guardar el proveedor
    else:
        form = ProveedorForm()  # Si no es una solicitud POST, crea un formulario vacío

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
    
def reabastecer_producto(request, producto_id):
    # Obtener el producto específico por su ID
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        cantidad_reabastecida = 10
        Reabastecimiento.objects.create(
                producto=producto,
                cantidad=cantidad_reabastecida,
                usuario=request.user
            ) 
        return redirect('inventario')

    # Si la solicitud no es POST, simplemente renderizamos la página nuevamente
    return render(request, 'tu_template.html', {'producto': producto})

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

def cancelar_reabastecimiento(request, reabastecimiento_id):
    reabastecimiento = get_object_or_404(Reabastecimiento, pk=reabastecimiento_id)
    if reabastecimiento.estado == 'pendiente':
        reabastecimiento.delete()
        messages.success(request, 'Reabastecimiento cancelado correctamente.')
    else:
        messages.error(request, 'No se puede cancelar un reabastecimiento confirmado.')
    return redirect('lista_reabastecimientos')

def realizar_venta(request, producto_id):
    if request.method == 'POST':
        producto = Producto.objects.get(pk=producto_id)
        cantidad_vendida = int(request.POST['cantidad'])
        if cantidad_vendida <= 0:
            messages.error(request, "La cantidad debe ser mayor que cero.")
            return redirect('inventario')
        if cantidad_vendida > producto.stock:
            messages.error(request, "No se puede vender más de lo que hay en el inventario.")
            return redirect('inventario')
        
        precio_unitario = producto.precio
        total = precio_unitario * cantidad_vendida
        
        # Crear la instancia de Venta después de calcular el total
        venta = Venta.objects.create(
            producto=producto,
            precio_unitario=precio_unitario,
            cantidad=cantidad_vendida,
            usuario=request.user
        )
        venta.total = total  # Asignar el total calculado a la instancia de venta
        venta.save()
        
        # Actualizar el stock del producto
        producto.stock -= cantidad_vendida
        producto.save()
        
        messages.success(request, "Venta realizada con éxito.")
        return redirect('inventario')

def lista_ventas(request):
    ventas_list = Venta.objects.all().order_by('-fecha_venta')
    paginator = Paginator(ventas_list, 10)  # Muestra 10 ventas por página

    page_number = request.GET.get('page')
    ventas = paginator.get_page(page_number)
    
    # Calcular el total de todas las ventas
    total_ventas = sum(venta.calcular_total() for venta in ventas_list)

    context = {
        'ventas': ventas,
        'total_ventas': total_ventas
    }
    return render(request, 'lista_ventas.html', context)


def generar_reporte_ventas_csv(request):
    ventas = Venta.objects.all()  # Obtener todas las ventas
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Producto', 'Precio Unitario', 'Cantidad', 'Total', 'Usuario', 'Fecha de Venta'])
    
    for venta in ventas:
        writer.writerow([venta.producto.nombre, venta.precio_unitario, venta.cantidad, venta.calcular_total(), venta.usuario.username, venta.fecha_venta])

    return response

def generar_reporte_ventas_pdf(request):
    ventas = Venta.objects.all()  # Obtener todas las ventas
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Reporte de Ventas")

    y = 730  # Posición inicial en y
    for venta in ventas:
        p.drawString(100, y, f"Producto: {venta.producto.nombre}")
        p.drawString(100, y - 20, f"Precio Unitario: ${venta.precio_unitario}")
        p.drawString(100, y - 40, f"Cantidad: {venta.cantidad}")
        p.drawString(100, y - 60, f"Total: ${venta.calcular_total()}")
        p.drawString(100, y - 80, f"Usuario: {venta.usuario.username}")
        p.drawString(100, y - 100, f"Fecha de Venta: {venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 120  # Espacio entre cada venta

    p.showPage()
    p.save()

    return response

def eliminar_reabastecimiento(request):
    # Eliminar todos los registros de ventas
    Reabastecimiento.objects.all().delete()
    # Redirigir a la página de la lista de ventas
    return redirect('lista_reabastecimientos')

def eliminar_ventas(request):
    # Eliminar todos los registros de ventas
    Venta.objects.all().delete()
    # Redirigir a la página de la lista de ventas
    return redirect('lista_ventas')


# def home_cliente(request):
#     return render(request, 'home_cliente.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def compras_cliente(request):
    return render(request, 'compras_cliente.html')

#============================ Modo Cliente =========================================
# def home_cliente(request):
#     return render(request, 'store/home.html')

def view_products(request):
    categories = Categoria.objects.all()
    products = Producto.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'store/products.html', context)

def get_products_by_category(request, category_id):
    print(category_id)
    categories = Categoria.objects.all()
    selected_category = Categoria.objects.get(id=category_id)
    products = Producto.objects.filter(categoria=selected_category)
    products_data = []
    for product in products:
        product_data = {
            "id": product.id,
            # "category": product.category,
            "name": product.name,
            "imageURL": product.imageURL,  # Assuming you have an imageURL field
            "price": product.price,
            # ... Add other product data you want to display
        }
        products_data.append(product_data)
    
    return JsonResponse(products_data, safe=False)  # Set safe=False if including non-string data

def view_cart(request):
    cart_items = OrderItem.objects.all()  # Assuming you have a CartItem model representing items in the cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    OrderItem.objects.create(product_id=product_id, quantity=1)
    return JsonResponse({'message': 'Product added to cart'})

def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    item = OrderItem.objects.get(id=item_id)
    item.delete()
    return redirect('view_cart')

def update_cart(request):
    item_id = request.GET.get('item_id')
    new_quantity = int(request.GET.get('quantity'))

    # Update the quantity of the item in the database
    item = OrderItem.objects.get(id=item_id)
    item.quantity = new_quantity
    item.save()

    # Return a JSON response indicating success
    return JsonResponse({'message': 'Cart updated successfully'})
