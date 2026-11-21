from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def store_home_view(request):
    # گرفتن همه دسته‌بندی‌ها (بازی‌ها و پلتفرم‌ها) برای صفحه اصلی فروشگاه
    categories = Category.objects.all()
    return render(request, 'Dstore/store_home.html', {'categories': categories})

def category_detail_view(request, category_slug):
    # پیدا کردن بازی یا پلتفرم انتخاب شده
    category = get_object_or_404(Category, slug=category_slug)
    
    # گرفتن همه محصولات مربوط به این دسته‌بندی
    products = Product.objects.filter(category=category, is_active=True)
    
    # جدا کردن محصولات بر اساس نوعشون (دقیقاً مثل عکس‌هایی که فرستادی)
    gems = products.filter(product_type='currency')
    passes = products.filter(product_type='battle_pass')
    offers = products.filter(product_type='special_offer')
    giftcards = products.filter(product_type='gift_card')

    context = {
        'category': category,
        'gems': gems,
        'passes': passes,
        'offers': offers,
        'giftcards': giftcards,
    }
    return render(request, 'Dstore/category_detail.html', context)
