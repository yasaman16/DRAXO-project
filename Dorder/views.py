
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Dstore.models import Product
from .models import Order, OrderItem
from django.contrib import messages

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    order, created = Order.objects.get_or_create(user=request.user, status='cart')
    
    order_item, item_created = OrderItem.objects.get_or_create(
        order=order, 
        product=product,
        defaults={'price': product.price, 'quantity': 1}
    )
    
    if not item_created:
        order_item.quantity += 1
        order_item.save()
        
    messages.success(request, f"محصول '{product.title}' به سبد خرید اضافه شد.")
    return redirect('Dorder:cart_detail')

@login_required
def cart_detail_view(request):
    order = Order.objects.filter(user=request.user, status='cart').first()
    return render(request, 'Dorder/cart.html', {'order': order})

@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if item.order.user == request.user:
        item.delete()
        messages.success(request, "محصول از سبد خرید حذف شد.")
    return redirect('Dorder:cart_detail')