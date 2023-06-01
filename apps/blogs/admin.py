from django.contrib import admin
from .models import Tag, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'image', 'category', 'author_name', 'author_image', 'created_date']


