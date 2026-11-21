from django.urls import path
from . import views

app_name = 'Dstore'

urlpatterns = [
    path('', views.store_home_view, name='store_home'),
    path('<slug:category_slug>/', views.category_detail_view, name='category_detail'),
]
