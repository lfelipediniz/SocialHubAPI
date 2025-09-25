from django.urls import path
from . import views

# explicit urls organized for better maintenance
urlpatterns = [
    # ============================================================================
    # REQUIRED BASIC ROUTES (from specification)
    # ============================================================================
    # list posts - optional batch system (batch_size, batch_number)
    path('', views.post_list, name='post-list'),
    # create post
    path('create/', views.post_create, name='post-create'),
    # post detail operations - GET (retrieve), PATCH (update), DELETE (remove)
    path('<int:pk>/', views.post_detail, name='post-detail'),
    
    # ============================================================================
    # ADDITIONAL SOCIAL INTERACTION ROUTES (my ideas to improve the project)
    # ============================================================================
    # likes
    path('<int:post_id>/like/', views.post_like, name='post-like'),
    path('<int:post_id>/unlike/', views.post_unlike, name='post-unlike'),
    path('<int:post_id>/likes/', views.post_likes_list, name='post-likes-list'),
    
    # comments
    path('<int:post_id>/comment/', views.post_comment, name='post-comment'),
    path('<int:post_id>/comments/', views.post_comments_list, name='post-comments-list'),
    
    # shares
    path('<int:post_id>/share/', views.post_share, name='post-share'),
    path('<int:post_id>/shares/', views.post_shares_list, name='post-shares-list'),
]

