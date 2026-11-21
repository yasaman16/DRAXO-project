from django.db import models
from django.conf import settings
from Dstore.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'سبد خرید'),
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'تکمیل شده'),
        ('canceled', 'لغو شده'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"سفارش {self.id} - {self.user.username} ({self.get_status_display()})"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=0) # قیمت لحظه خرید

    def str(self):
        return f"{self.quantity} x {self.product.title}"

    def get_cost(self):
        return self.price * self.quantity

