from django.db import models
from django.utils import timezone


class User(models.Model):
    # user model to ensure unique usernames
    username = models.CharField(max_length=100, unique=True, help_text="Unique username")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="User creation timestamp")
    
    class Meta:
        ordering = ['username']
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.username


class Post(models.Model):
    # post model for socialhubapi with all required fields and computed counts
    
    POST_TYPES = [
        ('original', 'Original Post'),
        ('shared', 'Shared Post'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', help_text="Author user", null=True, blank=True)
    title = models.CharField(max_length=200, help_text="Post title")
    content = models.TextField(help_text="Post content")
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='original', help_text="Type of post")
    original_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='shares', help_text="Original post if this is a shared post")
    share_comment = models.TextField(blank=True, help_text="Additional comment when sharing")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    
    class Meta:
        ordering = ['-created_datetime']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        if self.post_type == 'shared':
            return f"{self.user.username} shared: {self.original_post.title if self.original_post else 'Unknown'}"
        return f"{self.user.username}: {self.title}"

    @property
    def likes_count(self):
        # return the number of likes for this post
        return self.likes.count()

    @property
    def comments_count(self):
        # return the number of comments for this post
        return self.comments.count()

    @property
    def shares_count(self):
        # return the number of shares for this post
        return self.share_actions.count()

    @property
    def original_author(self):
        # return the original author if this is a shared post
        if self.post_type == 'shared' and self.original_post:
            return self.original_post.user.username
        return self.user.username

    @property
    def original_content(self):
        # return the original content if this is a shared post
        if self.post_type == 'shared' and self.original_post:
            return self.original_post.content
        return self.content

    @property
    def original_title(self):
        # return the original title if this is a shared post
        if self.post_type == 'shared' and self.original_post:
            return self.original_post.title
        return self.title


class Like(models.Model):
    # like model for posts with foreign key to post and user
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the like was created")
    
    class Meta:
        unique_together = ['post', 'user']  # prevent duplicate likes from same user
        ordering = ['-created_datetime']
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Comment(models.Model):
    # comment model for posts with foreign key to post, user and content
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField(help_text="Comment content")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the comment was created")
    
    class Meta:
        ordering = ['created_datetime']  # oldest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"


class Share(models.Model):
    # share model for posts with foreign key to post and user
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='share_actions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares', null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the share was created")
    
    class Meta:
        unique_together = ['post', 'user']  # prevent duplicate shares from same user
        ordering = ['-created_datetime']
        verbose_name = "Share"
        verbose_name_plural = "Shares"

    def __str__(self):
        return f"{self.user.username} shared {self.post.title}"