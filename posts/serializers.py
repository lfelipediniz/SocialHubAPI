from rest_framework import serializers
from .models import Post, Like, Comment, Share


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
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content', 'post_type', 'original_post', 'share_comment', 'created_datetime', 'likes_count', 'comments_count', 'shares_count', 'original_author', 'original_content', 'original_title', 'is_liked']
        read_only_fields = ['id', 'username', 'created_datetime', 'likes_count', 'comments_count', 'shares_count', 'original_author', 'original_content', 'original_title', 'is_liked']
    
    def get_is_liked(self, obj):
        # check if the current user has liked this post
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Título não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 200:
            raise serializers.ValidationError(f"Título muito longo! Máximo 200 caracteres. Atual: {len(value)} caracteres.")
        
        return value
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Conteúdo não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 5000:
            raise serializers.ValidationError(f"Conteúdo muito longo! Máximo 5000 caracteres. Atual: {len(value)} caracteres.")
        
        return value
    
    def validate_username(self, value):
        # validate username field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()


class PostCreateSerializer(serializers.ModelSerializer):
    # serializer for creating new posts, uses authenticated user
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def create(self, validated_data):
        # use authenticated user from request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Título não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 200:
            raise serializers.ValidationError(f"Título muito longo! Máximo 200 caracteres. Atual: {len(value)} caracteres.")
        
        return value
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Conteúdo não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 5000:
            raise serializers.ValidationError(f"Conteúdo muito longo! Máximo 5000 caracteres. Atual: {len(value)} caracteres.")
        
        return value


class PostUpdateSerializer(serializers.ModelSerializer):
    # serializer for updating existing posts, only title and content can be updated
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        # validate title field
        if not value or not value.strip():
            raise serializers.ValidationError("Título não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 200:
            raise serializers.ValidationError(f"Título muito longo! Máximo 200 caracteres. Atual: {len(value)} caracteres.")
        
        return value
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Conteúdo não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 5000:
            raise serializers.ValidationError(f"Conteúdo muito longo! Máximo 5000 caracteres. Atual: {len(value)} caracteres.")
        
        return value


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
    
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.CharField(write_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'username', 'user', 'content', 'created_datetime']
        read_only_fields = ['id', 'username', 'created_datetime']
    
    def validate_content(self, value):
        # validate content field
        if not value or not value.strip():
            raise serializers.ValidationError("Conteúdo não pode estar vazio.")
        
        value = value.strip()
        if len(value) > 1000:
            raise serializers.ValidationError(f"Comentário muito longo! Máximo 1000 caracteres. Atual: {len(value)} caracteres.")
        
        return value
    
    def validate_user(self, value):
        # validate user field
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()
    
    def create(self, validated_data):
        # get or create user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = validated_data.pop('user')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        
        # create comment with user
        return Comment.objects.create(user=user, **validated_data)


class ShareSerializer(serializers.ModelSerializer):
    # serializer for share model with post information
    
    username = serializers.CharField(source='user.username', read_only=True)
    shared_post_id = serializers.IntegerField(source='post.id', read_only=True)
    shared_post_title = serializers.CharField(source='post.title', read_only=True)
    shared_post_content = serializers.CharField(source='post.content', read_only=True)
    shared_post_author = serializers.CharField(source='post.user.username', read_only=True)
    shared_post_created = serializers.DateTimeField(source='post.created_datetime', read_only=True)
    
    class Meta:
        model = Share
        fields = [
            'id', 
            'username', 
            'created_datetime',
            'shared_post_id',
            'shared_post_title',
            'shared_post_content', 
            'shared_post_author',
            'shared_post_created'
        ]
        read_only_fields = [
            'id', 
            'username', 
            'created_datetime',
            'shared_post_id',
            'shared_post_title',
            'shared_post_content',
            'shared_post_author', 
            'shared_post_created'
        ]


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