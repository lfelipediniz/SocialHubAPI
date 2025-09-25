from django.contrib import admin
from .models import User, Post, Like, Comment, Share


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model."""
    
    list_display = ['id', 'username', 'created_datetime']
    list_filter = ['created_datetime']
    search_fields = ['username']
    readonly_fields = ['id', 'created_datetime']
    ordering = ['username']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""
    
    list_display = ['id', 'user', 'title', 'post_type', 'created_datetime']
    list_filter = ['created_datetime', 'post_type', 'user']
    search_fields = ['user__username', 'title', 'content']
    readonly_fields = ['id', 'created_datetime']
    ordering = ['-created_datetime']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'title', 'content', 'post_type')
        }),
        ('Sharing Information', {
            'fields': ('original_post', 'share_comment'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_datetime',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin interface for Like model."""
    
    list_display = ['id', 'user', 'post', 'created_datetime']
    list_filter = ['created_datetime', 'user']
    search_fields = ['user__username', 'post__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    
    list_display = ['id', 'user', 'post', 'created_datetime']
    list_filter = ['created_datetime', 'user']
    search_fields = ['user__username', 'post__title', 'content']


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    """Admin interface for Share model."""
    
    list_display = ['id', 'user', 'post', 'created_datetime']
    list_filter = ['created_datetime', 'user']
    search_fields = ['user__username', 'post__title']