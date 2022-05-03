from django.contrib import admin
from .models import Game, Move
# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_user', 'second_user', 'status']
    list_editable = ('status',)

@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('x', 'y', 'comments', 'by_first_user', 'game')


#admin.site.register(Game)
#admin.site.register(Move)