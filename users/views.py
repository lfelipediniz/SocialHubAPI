from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.conf import settings
from django_filters import rest_framework as django_filters
from datetime import datetime, timedelta

from .models import User, Follow
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    FollowSerializer,
    FollowCreateSerializer,
    UserListSerializer,
    SimpleUserRegistrationSerializer,
    SimpleUserLoginSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    view for user registration
    supports both full authentication and simple username-only modes
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        return UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # return token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserDetailSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """
    view for user login with JWT authentication
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """
    view for user logout with JWT token blacklisting
    """
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'message': 'successfully logged out'})
    except Exception as e:
        return Response({'error': f'error logging out: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_refresh(request):
    """
    view for refreshing JWT token
    """
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),
        })
    except Exception as e:
        return Response({'error': f'invalid refresh token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_list(request):
    """
    get /users/ - list users with optional batch system and filtering
    parameters: batch_size (max users per batch), batch_number (batch number, default 0)
    additional filters: search, first_name, last_name, ordering
    """
    from django.db.models import Q
    
    # get base queryset
    users = User.objects.all()
    
    # apply search filter
    search_query = request.query_params.get('search', None)
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # apply name filters
    first_name = request.query_params.get('first_name', None)
    if first_name:
        users = users.filter(first_name__icontains=first_name)
    
    last_name = request.query_params.get('last_name', None)
    if last_name:
        users = users.filter(last_name__icontains=last_name)
    
    # apply ordering
    ordering = request.query_params.get('ordering', 'username')
    if ordering in ['username', 'created_at', 'first_name', 'last_name']:
        users = users.order_by(ordering)
    else:
        users = users.order_by('username')  # default ordering
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        users_batch = users[start_index:end_index]
        
        # calculate total users for response info
        total_users = users.count()
        total_batches = (total_users + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = UserListSerializer(users_batch, many=True)
        return Response({
            'message': 'Users retrieved successfully',
            'users': serializer.data,
            'batch_info': {
                'current_batch': batch_number,
                'batch_size': batch_size,
                'total_users': total_users,
                'total_batches': total_batches,
                'users_in_current_batch': len(serializer.data)
            }
        })
    else:
        # return all users without batching
        serializer = UserListSerializer(users, many=True)
        return Response({
            'message': 'All users retrieved successfully',
            'users': serializer.data,
            'total_users': users.count()
        })




class UserProfileView(generics.RetrieveAPIView):
    """
    view for retrieving user profile (public information)
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    view for retrieving and updating user details (private information)
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    view for updating user profile
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class FollowListView(generics.ListAPIView):
    """
    view for listing users that the current user follows
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # get users that the current user follows
        following_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_ids)


class FollowersListView(generics.ListAPIView):
    """
    view for listing user's followers
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # check if username is provided in kwargs (for specific user)
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)
        else:
            # for current user (requires authentication)
            if not self.request.user.is_authenticated:
                return User.objects.none()
            user = self.request.user
        
        # get users who follow this user (followers)
        follower_ids = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)


class FollowingListView(generics.ListAPIView):
    """
    view for listing users that a user follows
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        # fix: get users that this user follows (following)
        following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_ids)


class FollowCreateView(generics.CreateAPIView):
    """
    view for creating follow relationships
    """
    serializer_class = FollowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, username):
    """
    view for unfollowing a user
    """
    try:
        user_to_unfollow = get_object_or_404(User, username=username)
        follow = Follow.objects.get(follower=request.user, following=user_to_unfollow)
        follow.delete()
        return Response({'message': f'stopped following {username}'})
    except Follow.DoesNotExist:
        return Response(
            {'error': f'not following {username}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    view for getting user statistics
    """
    user = request.user
    stats = {
        'posts_count': user.posts_count,
        'followers_count': user.followers_count,
        'following_count': user.following_count,
        'likes_received': user.posts.aggregate(
            total_likes=models.Count('likes')
        )['total_likes'] or 0,
        'comments_received': user.posts.aggregate(
            total_comments=models.Count('comments')
        )['total_comments'] or 0,
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_user_stats(request, username):
    """
    view for getting public user statistics (no authentication required)
    """
    try:
        user = User.objects.get(username=username)
        stats = {
            'posts_count': user.posts_count,
            'followers_count': user.followers_count,
            'following_count': user.following_count,
            'likes_received': user.posts.aggregate(
                total_likes=models.Count('likes')
            )['total_likes'] or 0,
            'comments_received': user.posts.aggregate(
                total_comments=models.Count('comments')
            )['total_comments'] or 0,
        }
        return Response(stats)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

