from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    """
    Custom user model with additional fields for social features
    """
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text="Required. 3-30 characters. Letters, digits and @/./+/-/_ only."
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # social features
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        through='Follow'
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @property
    def posts_count(self):
        """return total number of posts by this user"""
        return self.posts.count()
    
    @property
    def followers_count(self):
        """return number of followers"""
        return self.follower_relationships.count()
    
    @property
    def following_count(self):
        """return number of users this user follows"""
        return self.following_relationships.count()


class Follow(models.Model):
    """
    Intermediate model for user following relationships
    """
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_relationships'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relationships'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users_follow'
        unique_together = ['follower', 'following']
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
    
    def save(self, *args, **kwargs):
        # prevent self-following
        if self.follower == self.following:
            raise ValueError("users cannot follow themselves")
        super().save(*args, **kwargs)