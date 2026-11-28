from django.urls import path

from . import views

app_name = 'Dpages'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('game-calendar/', views.game_calendar_view, name='game_calendar'),
    path('games/<slug:game_slug>/', views.game_detail_view, name='game_detail'),
]
