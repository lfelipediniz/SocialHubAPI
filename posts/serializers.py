from rest_framework import serializers
from .models import User, Post, Like, Comment, Share


# ============================================================================
# SERIALIZERS FOR USERS
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    # serializer for user model
    
    class Meta:
        model = User
        fields = ['id', 'username', 'created_datetime']
        read_only_fields = ['id', 'created_datetime']
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()


# ============================================================================
# SERIALIZERS FOR POSTS
# ============================================================================

class PostSerializer(serializers.ModelSerializer):
    # serializer for post model with proper field validation and read-only field handling
    
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    shares_count = serializers.ReadOnlyField()
    original_author = serializers.ReadOnlyField()
    original_content = serializers.ReadOnlyField()
    original_title = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content', 'post_type', 'original_post', 'share_comment', 'created_datetime', 'likes_count', 'comments_count', 'shares_count', 'original_author', 'original_content', 'original_title']
        read_only_fields = ['id', 'username', 'created_datetime', 'likes_count', 'comments_count', 'shares_count', 'original_author', 'original_content', 'original_title']
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()


class PostCreateSerializer(serializers.ModelSerializer):
    # serializer for creating new posts, all fields except id and created_datetime are required
    
    username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Post
        fields = ['username', 'title', 'content']
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()
    
    def create(self, validated_data):
        # get or create user
        username = validated_data.pop('username')
        user, created = User.objects.get_or_create(username=username)
        
        # create post with user
        return Post.objects.create(user=user, **validated_data)
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()


class PostUpdateSerializer(serializers.ModelSerializer):
    # serializer for updating existing posts, only title and content can be updated
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()


# ============================================================================
# SERIALIZERS FOR SOCIAL INTERACTIONS (my implementation)
# ============================================================================

class LikeSerializer(serializers.ModelSerializer):
    # serializer for like model
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'username', 'created_datetime']
        read_only_fields = ['id', 'username', 'created_datetime']


class CommentSerializer(serializers.ModelSerializer):
    # serializer for comment model
    
    username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'created_datetime']
        read_only_fields = ['id', 'created_datetime']
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()
    
    def create(self, validated_data):
        # get or create user
        username = validated_data.pop('username')
        user, created = User.objects.get_or_create(username=username)
        
        # create comment with user
        return Comment.objects.create(user=user, **validated_data)


class ShareSerializer(serializers.ModelSerializer):
    # serializer for share model
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Share
        fields = ['id', 'username', 'created_datetime']
        read_only_fields = ['id', 'username', 'created_datetime']


class PostShareSerializer(serializers.ModelSerializer):
    # serializer for sharing posts with additional comment
    
    username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Post
        fields = ['username', 'share_comment']
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()
    
    def validate_share_comment(self, value):
        # validate share comment field (optional)
        if value:
            return value.strip()
        return value