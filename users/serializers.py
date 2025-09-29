from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from .models import User, Follow


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'min_length': 3},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('user account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializer for user profile (public information)
    """
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'bio', 'avatar',
            'created_at', 'posts_count', 'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'username', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    serializer for detailed user information (private)
    """
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'avatar',
            'created_at', 'updated_at', 'posts_count', 'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    serializer for updating user profile
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'email']
    
    def validate_email(self, value):
        # check if email is already taken by another user
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("email already exists")
        return value


class FollowSerializer(serializers.ModelSerializer):
    """
    serializer for follow relationships
    """
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'follower_username', 'following_username', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']


class FollowCreateSerializer(serializers.ModelSerializer):
    """
    serializer for creating follow relationships
    """
    class Meta:
        model = Follow
        fields = ['following']
    
    def validate_following(self, value):
        # prevent self-following
        if value == self.context['request'].user:
            raise serializers.ValidationError("cannot follow yourself")
        
        # check if already following
        if Follow.objects.filter(
            follower=self.context['request'].user,
            following=value
        ).exists():
            raise serializers.ValidationError("already following this user")
        
        return value
    
    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)


class UserListSerializer(serializers.ModelSerializer):
    """
    serializer for user list (minimal information)
    """
    is_following = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'is_following']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user,
                following=obj
            ).exists()
        return False
    
    def get_first_name(self, obj):
        """return null if first_name is empty string"""
        return obj.first_name if obj.first_name.strip() else None
    
    def get_last_name(self, obj):
        """return null if last_name is empty string"""
        return obj.last_name if obj.last_name.strip() else None




# Simple mode serializers (when AUTHENTICATION_REQUIRED=False)
class SimpleUserRegistrationSerializer(serializers.ModelSerializer):
    """
    simple user registration without password validation
    used when AUTHENTICATION_REQUIRED=False
    """
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar']
        extra_kwargs = {
            'username': {'min_length': 3},
            'email': {'required': False}
        }
    
    def create(self, validated_data):
        # create user with dummy password when authentication is not required
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', f"{validated_data['username']}@example.com"),
            password='dummy_password_not_used',  # dummy password
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            avatar=validated_data.get('avatar', '')
        )
        return user


class SimpleUserLoginSerializer(serializers.Serializer):
    """
    simple user login without password
    used when AUTHENTICATION_REQUIRED=False
    """
    username = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        
        if not username:
            raise serializers.ValidationError('username is required')
        
        try:
            # get or create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'is_active': True,
                }
            )
            attrs['user'] = user
        except Exception as e:
            raise serializers.ValidationError(f'error creating user: {str(e)}')
        
        return attrs
