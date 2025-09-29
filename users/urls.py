from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    
    # JWT token refresh
    path('token/refresh/', views.token_refresh, name='token-refresh'),
    
    # user management endpoints
    path('', views.user_list, name='user-list'),
    path('me/', views.UserDetailView.as_view(), name='user-detail'),
    path('me/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('me/stats/', views.user_stats, name='user-stats'),
    
    # follow/unfollow endpoints
    path('follow/', views.FollowCreateView.as_view(), name='follow-create'),
    path('following/', views.FollowListView.as_view(), name='follow-list'),
    path('followers/', views.FollowersListView.as_view(), name='followers-list'),
    
    # user-specific endpoints (must come after generic ones)
    path('<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('<str:username>/stats/', views.public_user_stats, name='public-user-stats'),
    path('<str:username>/followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following-list'),
    path('<str:username>/unfollow/', views.unfollow_user, name='unfollow-user'),
]
