from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
import json

from .models import User, Follow
from posts.models import Post, Like, Comment, Share

User = get_user_model()


class UserModelTests(TestCase):
    """test user model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """test basic user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.check_password('wrongpass'))
    
    def test_user_str_representation(self):
        """test user string representation"""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_posts_count_property(self):
        """test posts count property"""
        # initially should be 0
        self.assertEqual(self.user.posts_count, 0)
        
        # create a post
        Post.objects.create(
            user=self.user,
            title='Test Post',
            content='Test content'
        )
        
        # should now be 1
        self.assertEqual(self.user.posts_count, 1)
    
    def test_user_followers_count_property(self):
        """test followers count property"""
        # initially should be 0
        self.assertEqual(self.user.followers_count, 0)
        
        # create another user and follow
        follower = User.objects.create_user(
            username='follower',
            email='follower@example.com',
            password='testpass123'
        )
        Follow.objects.create(follower=follower, following=self.user)
        
        # should now be 1
        self.assertEqual(self.user.followers_count, 1)
    
    def test_user_following_count_property(self):
        """test following count property"""
        # initially should be 0
        self.assertEqual(self.user.following_count, 0)
        
        # create another user and follow
        following = User.objects.create_user(
            username='following',
            email='following@example.com',
            password='testpass123'
        )
        Follow.objects.create(follower=self.user, following=following)
        
        # should now be 1
        self.assertEqual(self.user.following_count, 1)


class FollowModelTests(TestCase):
    """test follow model functionality"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
    
    def test_follow_creation(self):
        """test basic follow creation"""
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertIsNotNone(follow.created_at)
    
    def test_follow_str_representation(self):
        """test follow string representation"""
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        expected = f'{self.user1.username} follows {self.user2.username}'
        self.assertEqual(str(follow), expected)
    
    def test_self_follow_prevention(self):
        """test that users cannot follow themselves"""
        with self.assertRaises(ValueError):
            Follow.objects.create(
                follower=self.user1,
                following=self.user1
            )
    
    def test_unique_follow_constraint(self):
        """test that duplicate follows are prevented"""
        # create first follow
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        
        # try to create duplicate follow
        with self.assertRaises(Exception):  # integrity error
            Follow.objects.create(
                follower=self.user1,
                following=self.user2
            )


class UserRegistrationTests(APITestCase):
    """test user registration functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:user-register')
    
    def test_successful_registration(self):
        """test successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
        
        # verify user was created in database
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # verify token was created
        user = User.objects.get(username='newuser')
        self.assertTrue(Token.objects.filter(user=user).exists())
    
    def test_registration_password_mismatch(self):
        """test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'differentpass123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('passwords do not match', str(response.data))
    
    def test_registration_duplicate_username(self):
        """test registration with duplicate username"""
        # create existing user
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        
        data = {
            'username': 'existing',
            'email': 'newemail@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_registration_duplicate_email(self):
        """test registration with duplicate email"""
        # create existing user
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_registration_missing_required_fields(self):
        """test registration with missing required fields"""
        # missing username
        data = {
            'email': 'test@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # missing email
        data = {
            'username': 'testuser',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # missing password
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_short_username(self):
        """test registration with username too short"""
        data = {
            'username': 'ab',  # less than 3 characters
            'email': 'test@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_long_username(self):
        """test registration with username too long"""
        data = {
            'username': 'a' * 31,  # more than 30 characters
            'email': 'test@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_invalid_email(self):
        """test registration with invalid email format"""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_weak_password(self):
        """test registration with weak password"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123',  # too short
            'password_confirm': '123'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(APITestCase):
    """test user login functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('users:user-login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_successful_login(self):
        """test successful user login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        
        # verify token was created
        self.assertTrue(Token.objects.filter(user=self.user).exists())
    
    def test_login_invalid_username(self):
        """test login with invalid username"""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('invalid credentials', str(response.data))
    
    def test_login_invalid_password(self):
        """test login with invalid password"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('invalid credentials', str(response.data))
    
    def test_login_missing_credentials(self):
        """test login with missing credentials"""
        # missing username
        data = {'password': 'testpass123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # missing password
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # missing both
        data = {}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_empty_credentials(self):
        """test login with empty credentials"""
        data = {
            'username': '',
            'password': ''
        }
        
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_inactive_user(self):
        """test login with inactive user"""
        self.user.is_active = False
        self.user.save()
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # inactive users return 'invalid credentials' because authenticate returns None
        self.assertIn('invalid credentials', str(response.data))


class UserLogoutTests(APITestCase):
    """test user logout functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('users:user-logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_successful_logout(self):
        """test successful user logout"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('successfully logged out', response.data['message'])
        
        # verify token was deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())
    
    def test_logout_without_token(self):
        """test logout without authentication token"""
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout_invalid_token(self):
        """test logout with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-token')
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)