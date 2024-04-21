from django.db import models

# Create your models here.
class Customer(models.Model): 
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    phone = models.CharField(max_length=10) 
    email = models.EmailField() 
    
class Category(models.Model): 
    name = models.CharField(max_length=50) 
  
    def __str__(self): 
        return self.name 
    
    def get_category_id(self):
        return self.id
    
class Product(models.Model): 
    name = models.CharField(max_length=60) 
    price = models.IntegerField(default=0) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    description = models.CharField(max_length=250, default='', blank=True, null=True) 
    image = models.ImageField(null=True, blank=True)
    expiration_date = models.DateField()

    def __str__(self):
          return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    