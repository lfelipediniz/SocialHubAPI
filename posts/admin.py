from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""
    
    list_display = ['id', 'username', 'title', 'created_datetime']
    list_filter = ['created_datetime', 'username']
    search_fields = ['username', 'title', 'content']
    readonly_fields = ['id', 'created_datetime']
    ordering = ['-created_datetime']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'username', 'title', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_datetime',),
            'classes': ('collapse',)
        }),
    )