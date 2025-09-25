from django.db import models
from django.utils import timezone


class Post(models.Model):
    # post model for codeleap careers api with all required fields and computed counts
    
    username = models.CharField(max_length=100, help_text="Author username")
    title = models.CharField(max_length=200, help_text="Post title")
    content = models.TextField(help_text="Post content")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    
    class Meta:
        ordering = ['-created_datetime']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return f"{self.username}: {self.title}"
    
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
        return self.shares.count()


class Like(models.Model):
    # like model for posts with foreign key to post and username
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    username = models.CharField(max_length=100, help_text="Username of the user who liked")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the like was created")
    
    class Meta:
        unique_together = ['post', 'username']  # prevent duplicate likes from same user
        ordering = ['-created_datetime']
        verbose_name = "Like"
        verbose_name_plural = "Likes"
    
    def __str__(self):
        return f"{self.username} liked {self.post.title}"


class Comment(models.Model):
    # comment model for posts with foreign key to post, username and content
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=100, help_text="Username of the commenter")
    content = models.TextField(help_text="Comment content")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the comment was created")
    
    class Meta:
        ordering = ['created_datetime']  # oldest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f"{self.username} commented on {self.post.title}"


class Share(models.Model):
    # share model for posts with foreign key to post and username
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    username = models.CharField(max_length=100, help_text="Username of the user who shared")
    created_datetime = models.DateTimeField(auto_now_add=True, help_text="When the share was created")
    
    class Meta:
        unique_together = ['post', 'username']  # prevent duplicate shares from same user
        ordering = ['-created_datetime']
        verbose_name = "Share"
        verbose_name_plural = "Shares"
    
    def __str__(self):
        return f"{self.username} shared {self.post.title}"