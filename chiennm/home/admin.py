from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'tags')
    list_filter = ('created_at', 'updated_at', 'author')
    ordering = ('-created_at',)
