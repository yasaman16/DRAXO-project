from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    PRODUCT_TYPES = (
        ('currency', 'ارز درون بازی (CP/UC/Gems)'),
        ('battle_pass', 'بتل پس / پاس'),
        ('special_offer', 'پیشنهاد ویژه / آفر'),
        ('gift_card', 'گیفت کارت'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.title} ({self.category.name})"

    class Meta:
        ordering = ['-created_at']