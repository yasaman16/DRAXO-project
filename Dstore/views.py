from django.shortcuts import render, get_object_or_404
from .models import Category

def store_home_view(request):
    # گرفتن همه دسته‌بندی‌ها (بازی‌ها و پلتفرم‌ها) برای صفحه اصلی فروشگاه
    categories = Category.objects.all()
    return render(request, 'Dstore/store_home.html', {'categories': categories})

def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    sections = {
        'currency': '??? ???? ????',
        'battle_pass': '🎫 بتل پس / پاس',
        'special_offer': '🔥 آفرها و پیشنهادهای ویژه',
        'gift_card': '🎁 گیفت کارت\u200cها',
    }
    products_by_type = {kind: [] for kind in sections}
    for product in category.products.filter(is_active=True, product_type__in=sections):
        products_by_type[product.product_type].append(product)

    product_sections = [
        (title, products_by_type[kind])
        for kind, title in sections.items()
        if products_by_type[kind]
    ]
    return render(request, 'Dstore/category_detail.html', {
        'category': category,
        'product_sections': product_sections,
    })
