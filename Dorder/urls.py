from django.urls import path
from . import views

app_name = 'Dorder'

urlpatterns = [
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
]
