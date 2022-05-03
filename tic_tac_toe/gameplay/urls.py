from django.urls import path
from .views import game_detail, make_move
urlpatterns = [
    path('detail/<int:id>', game_detail, name='game_detail'),
    path('make_move/<int:id>', make_move, name='make_move'),
]