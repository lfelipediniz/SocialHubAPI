from rest_framework import serializers
from .models import Post, Like, Comment, Share


# ============================================================================
# SERIALIZERS FOR POSTS
# ============================================================================

class PostSerializer(serializers.ModelSerializer):
    # serializer for post model with proper field validation and read-only field handling
    
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    shares_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content', 'created_datetime', 'likes_count', 'comments_count', 'shares_count']
        read_only_fields = ['id', 'created_datetime', 'likes_count', 'comments_count', 'shares_count']
    
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
    
    class Meta:
        model = Post
        fields = ['username', 'title', 'content']
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()
    
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
    
    class Meta:
        model = Like
        fields = ['id', 'username', 'created_datetime']
        read_only_fields = ['id', 'created_datetime']


class CommentSerializer(serializers.ModelSerializer):
    # serializer for comment model
    
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


class ShareSerializer(serializers.ModelSerializer):
    # serializer for share model
    
    class Meta:
        model = Share
        fields = ['id', 'username', 'created_datetime']
        read_only_fields = ['id', 'created_datetime']