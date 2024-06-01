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

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, through='ProductoCategoria')

    def __str__(self):
        return self.nombre

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

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=100)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nombre} - Estado: {self.estado_pedido}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.pedido.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"
    
class HistorialCambioProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(default=datetime.now)
    campo_modificado = models.CharField(max_length=100)
    valor_anterior = models.CharField(max_length=255)
    valor_nuevo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.producto.nombre} - {self.campo_modificado} - {self.fecha_cambio}"
    
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

