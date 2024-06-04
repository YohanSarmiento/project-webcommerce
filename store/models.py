from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    def get_category_id(self):
        return self.id

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, through='ProductoCategoria')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Nuevo campo de imagen

    def __str__(self):
        return self.nombre
    
    @property
    def imageURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url
    


class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    contraseña = models.CharField(max_length=100)
    es_cliente = models.BooleanField(default=True)  # Indica si es un cliente
    es_administrador = models.BooleanField(default=False)  # Indica si es un administrador

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# class Pedido(models.Model):
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     fecha_pedido = models.DateTimeField(auto_now_add=True)
#     estado_pedido = models.CharField(max_length=100)

#     def __str__(self):
#         return f"Pedido {self.id} - Cliente: {self.cliente.nombre} - Estado: {self.estado_pedido}"

# class DetallePedido(models.Model):
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cantidad = models.IntegerField()
    
#     precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Pedido {self.pedido.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"
    
class Order(models.Model):
    customer = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 


class OrderItem(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class HistorialCambioProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    campo_modificado = models.CharField(max_length=100)
    valor_anterior = models.TextField()  # Cambiar a TextField para valores largos
    valor_nuevo = models.TextField()     # Cambiar a TextField para valores largos

    def __str__(self):
        return f"{self.fecha_cambio.strftime('%Y-%m-%d %H:%M:%S')} - {self.usuario.username} - {self.campo_modificado}"
    
@receiver(pre_save, sender=Producto)
def registrar_cambio_producto(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Producto.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(instance, field_name)
            if old_value != new_value:
                # Registra el cambio en el historial
                HistorialCambioProducto.objects.create(
                    producto=instance,
                    usuario=User.objects.first(),  # Aquí deberías especificar el usuario que realiza el cambio
                    campo_modificado=field.verbose_name,
                    valor_anterior=str(old_value),
                    valor_nuevo=str(new_value)
                )
                
class ProductoCambio(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(default=datetime.now)
    nombre_anterior = models.CharField(max_length=255, blank=True, null=True)
    nombre_nuevo = models.CharField(max_length=255, blank=True, null=True)
    descripcion_anterior = models.TextField(blank=True, null=True)
    descripcion_nueva = models.TextField(blank=True, null=True)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_anterior = models.IntegerField(blank=True, null=True)
    stock_nuevo = models.IntegerField(blank=True, null=True)
    proveedor_anterior = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, blank=True, null=True, related_name='proveedor_anterior')
    proveedor_nuevo = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, blank=True, null=True, related_name='proveedor_nuevo')
    categorias_anterior = models.ManyToManyField('Categoria', blank=True, related_name='categorias_anterior')
    categorias_nuevo = models.ManyToManyField('Categoria', blank=True, related_name='categorias_nuevo')
    imagen_anterior = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_nueva = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha_cambio}"

                
class Reabastecimiento(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
    ]
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades - {self.estado}"
    
class Venta(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User de Django
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"Venta de {self.cantidad} unidades de {self.producto.nombre} por {self.usuario.username}"


# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return str(self.id)

#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total 

#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total 


# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
 
#     @property
#     def get_total(self):
#         total = self.product.price * self.quantity
#         return total
