from django.db import models
from django.conf import settings

class PostCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ (آدرس)")

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = "دسته‌بندی پست‌ها"


class Post(models.Model):
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="دسته‌بندی")
    title = models.CharField(max_length=200, verbose_name="عنوان پست")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="اسلاگ (آدرس سئو)")
    summary = models.TextField(max_length=300, verbose_name="خلاصه پست (برای سئو)")
    content = models.TextField(verbose_name="متن اصلی پست")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="عکس کاور پست")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="نویسنده")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ آپدیت")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده؟")

    def str(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "پست‌ها (اخبار و مقالات)"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست مربوطه")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    body = models.TextField(verbose_name="متن کامنت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_active = models.BooleanField(default=True, verbose_name="تایید شده؟")

    def str(self):
        return f"کامنت {self.user.username} برای {self.post.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "کامنت‌ها"
        