from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import *
from .models import Category, Product
from django.http import JsonResponse
from django.shortcuts import redirect
from decimal import Decimal

def home(request):
    return render(request, 'store/home.html')

def view_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'store/products.html', context)

def get_products_by_category(request, category_id):
    print(category_id)
    categories = Category.objects.all()
    selected_category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=selected_category)
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