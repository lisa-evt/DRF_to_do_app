from django.contrib import admin

from .models import Board, Todo


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'done', 'created')
    list_filter = ('done',)
