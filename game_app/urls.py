from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_list, name='home'),  # <-- корень сайта показывает список игроков
    path('players/', views.player_list, name='player_list'),
    path('players/create/', views.player_create, name='player_create'),
    path('players/<int:pk>/edit/', views.player_update, name='player_update'),
    path('players/<int:pk>/delete/', views.player_delete, name='player_delete'),
    path('results/', views.result_list, name='result_list'),
    path('results/<int:pk>/edit/', views.result_update, name='result_update'),
    path('results/<int:pk>/delete/', views.result_delete, name='result_delete'),
    path('players/<int:player_id>/play/', views.play_game, name='play_game'),
]
