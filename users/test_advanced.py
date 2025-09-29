from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User, Follow
from posts.models import Post, Like, Comment, Share

User = get_user_model()


class UserProfileTests(APITestCase):
    """test user profile functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            bio='Test bio'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_get_current_user_profile(self):
        """test getting current user profile"""
        url = reverse('users:user-detail')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['bio'], 'Test bio')
        self.assertIn('posts_count', response.data)
        self.assertIn('followers_count', response.data)
        self.assertIn('following_count', response.data)
    
    def test_get_profile_without_auth(self):
        """test getting profile without authentication"""
        self.client.credentials()
        url = reverse('users:user-detail')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_user_profile(self):
        """test updating user profile"""
        url = reverse('users:user-update')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio',
            'avatar': 'https://example.com/avatar.jpg'
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')
        self.assertEqual(response.data['bio'], 'Updated bio')
        self.assertEqual(response.data['avatar'], 'https://example.com/avatar.jpg')
        
        # verify changes in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.bio, 'Updated bio')
    
    def test_update_email_duplicate(self):
        """test updating email to duplicate"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        url = reverse('users:user-update')
        data = {'email': 'other@example.com'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email already exists', str(response.data))
    
    def test_update_without_auth(self):
        """test updating profile without authentication"""
        self.client.credentials()
        url = reverse('users:user-update')
        data = {'bio': 'Updated bio'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_statistics(self):
        """test getting user statistics"""
        url = reverse('users:user-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('posts_count', response.data)
        self.assertIn('followers_count', response.data)
        self.assertIn('following_count', response.data)
        self.assertIn('likes_received', response.data)
        self.assertIn('comments_received', response.data)
    
    def test_get_stats_without_auth(self):
        """test getting stats without authentication"""
        self.client.credentials()
        url = reverse('users:user-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicUserProfileTests(APITestCase):
    """test public user profile functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='publicuser',
            email='public@example.com',
            password='testpass123',
            first_name='Public',
            last_name='User',
            bio='Public user bio'
        )
    
    def test_get_public_user_profile(self):
        """test getting public user profile"""
        url = reverse('users:user-profile', kwargs={'username': 'publicuser'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'publicuser')
        self.assertEqual(response.data['first_name'], 'Public')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['bio'], 'Public user bio')
        self.assertIn('posts_count', response.data)
        self.assertIn('followers_count', response.data)
        self.assertIn('following_count', response.data)
        # email should not be in public profile
        self.assertNotIn('email', response.data)
    
    def test_get_nonexistent_user_profile(self):
        """test getting profile of nonexistent user"""
        url = reverse('users:user-profile', kwargs={'username': 'nonexistent'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserListTests(APITestCase):
    """test user list functionality"""
    
    def setUp(self):
        self.client = APIClient()
        
        # create test users
        self.user1 = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='testpass123',
            first_name='Alice',
            last_name='Smith'
        )
        self.user2 = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='testpass123',
            first_name='Bob',
            last_name='Jones'
        )
        self.user3 = User.objects.create_user(
            username='charlie',
            email='charlie@example.com',
            password='testpass123',
            first_name='Charlie',
            last_name='Brown'
        )
    
    def test_list_all_users(self):
        """test listing all users"""
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)
        
        # check user data
        usernames = [user['username'] for user in response.data['results']]
        self.assertIn('alice', usernames)
        self.assertIn('bob', usernames)
        self.assertIn('charlie', usernames)
    
    def test_search_users_by_username(self):
        """test searching users by username"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'search': 'alice'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['username'], 'alice')
    
    def test_search_users_by_first_name(self):
        """test searching users by first name"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'search': 'Bob'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['username'], 'bob')
    
    def test_search_users_by_last_name(self):
        """test searching users by last name"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'search': 'Brown'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['username'], 'charlie')
    
    def test_filter_users_by_first_name(self):
        """test filtering users by first name"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'first_name': 'Alice'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['username'], 'alice')
    
    def test_filter_users_by_last_name(self):
        """test filtering users by last name"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'last_name': 'Jones'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['username'], 'bob')
    
    def test_ordering_users_by_username(self):
        """test ordering users by username"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'ordering': 'username'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [user['username'] for user in response.data['results']]
        self.assertEqual(usernames, ['alice', 'bob', 'charlie'])
    
    def test_ordering_users_by_created_at(self):
        """test ordering users by created_at"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'ordering': '-created_at'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should be ordered by most recent first
        usernames = [user['username'] for user in response.data['results']]
        self.assertEqual(usernames[0], 'charlie')  # created last
    
    def test_empty_search_results(self):
        """test search with no results"""
        url = reverse('users:user-list')
        response = self.client.get(url, {'search': 'nonexistent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)


class FollowTests(APITestCase):
    """test follow/unfollow functionality"""
    
    def setUp(self):
        self.client = APIClient()
        
        # clean up any existing follows before each test
        Follow.objects.all().delete()
        
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
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
    
    def tearDown(self):
        # clean up all follow relationships to prevent test interference
        Follow.objects.all().delete()
    
    def test_successful_follow(self):
        """test successful follow"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:follow-create')
        data = {'following': self.user2.id}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['following'], self.user2.id)
        
        # verify follow was created in database
        self.assertTrue(Follow.objects.filter(
            follower=self.user1,
            following=self.user2
        ).exists())
    
    def test_follow_without_auth(self):
        """test follow without authentication"""
        url = reverse('users:follow-create')
        data = {'following': self.user2.id}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_follow_self(self):
        """test trying to follow yourself"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:follow-create')
        data = {'following': self.user1.id}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot follow yourself', str(response.data))
    
    def test_follow_nonexistent_user(self):
        """test following nonexistent user"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:follow-create')
        data = {'following': 99999}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_duplicate_follow(self):
        """test trying to follow someone already followed"""
        # create existing follow
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:follow-create')
        data = {'following': self.user2.id}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already following', str(response.data))
    
    def test_successful_unfollow(self):
        """test successful unfollow"""
        # create follow first
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:unfollow-user', kwargs={'username': 'user2'})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stopped following user2', response.data['message'])
        
        # verify follow was deleted
        self.assertFalse(Follow.objects.filter(
            follower=self.user1,
            following=self.user2
        ).exists())
    
    def test_unfollow_without_auth(self):
        """test unfollow without authentication"""
        url = reverse('users:unfollow-user', kwargs={'username': 'user2'})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unfollow_not_following(self):
        """test unfollowing someone you're not following"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:unfollow-user', kwargs={'username': 'user2'})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('not following user2', str(response.data))
    
    def test_unfollow_nonexistent_user(self):
        """test unfollowing nonexistent user"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:unfollow-user', kwargs={'username': 'nonexistent'})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_following(self):
        """test listing users you follow"""
        # create follows
        Follow.objects.create(follower=self.user1, following=self.user2)
        Follow.objects.create(follower=self.user1, following=self.user3)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:follow-list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # fix: check results count, not total response data length
        self.assertEqual(len(response.data['results']), 2)
        
        following_ids = [follow['following'] for follow in response.data['results']]
        self.assertIn(self.user2.id, following_ids)
        self.assertIn(self.user3.id, following_ids)
    
    def test_list_following_without_auth(self):
        """test listing following without authentication"""
        url = reverse('users:follow-list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_user_followers(self):
        """test listing a user's followers"""
        # create follows
        Follow.objects.create(follower=self.user1, following=self.user2)
        Follow.objects.create(follower=self.user3, following=self.user2)
        
        url = reverse('users:followers-list', kwargs={'username': 'user2'})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        follower_usernames = [user['username'] for user in response.data['results']]
        self.assertIn('user1', follower_usernames)
        self.assertIn('user3', follower_usernames)
    
    def test_list_user_followers_nonexistent_user(self):
        """test listing followers of nonexistent user"""
        url = reverse('users:followers-list', kwargs={'username': 'nonexistent'})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_who_user_follows(self):
        """test listing who a user follows"""
        # create follows
        Follow.objects.create(follower=self.user1, following=self.user2)
        Follow.objects.create(follower=self.user1, following=self.user3)
        
        url = reverse('users:following-list', kwargs={'username': 'user1'})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        following_usernames = [user['username'] for user in response.data['results']]
        self.assertIn('user2', following_usernames)
        self.assertIn('user3', following_usernames)
    
    def test_list_who_user_follows_nonexistent_user(self):
        """test listing who nonexistent user follows"""
        url = reverse('users:following-list', kwargs={'username': 'nonexistent'})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserFeedTests(APITestCase):
    """test user feed functionality"""
    
    def setUp(self):
        self.client = APIClient()
        
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
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        self.token1 = Token.objects.create(user=self.user1)
        
        # create posts
        self.post1 = Post.objects.create(
            user=self.user1,
            title='User1 Post 1',
            content='Content 1'
        )
        self.post2 = Post.objects.create(
            user=self.user2,
            title='User2 Post 1',
            content='Content 2'
        )
        self.post3 = Post.objects.create(
            user=self.user3,
            title='User3 Post 1',
            content='Content 3'
        )
    
    def test_get_user_feed_with_follows(self):
        """test getting user feed with followed users"""
        # user1 follows user2
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:user-feed')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_info']['total_posts'], 2)  # user1's post + user2's post
        
        post_titles = [post['title'] for post in response.data['posts']]
        self.assertIn('User1 Post 1', post_titles)
        self.assertIn('User2 Post 1', post_titles)
        self.assertNotIn('User3 Post 1', post_titles)
    
    def test_get_user_feed_without_follows(self):
        """test getting user feed without any follows"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:user-feed')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_info']['total_posts'], 1)  # only user1's own posts
        
        post_titles = [post['title'] for post in response.data['posts']]
        self.assertIn('User1 Post 1', post_titles)
        self.assertNotIn('User2 Post 1', post_titles)
        self.assertNotIn('User3 Post 1', post_titles)
    
    def test_get_feed_without_auth(self):
        """test getting feed without authentication"""
        url = reverse('users:user-feed')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_feed_ordering(self):
        """test that feed is ordered by most recent first"""
        # create more posts with different timestamps
        import time
        time.sleep(0.01)  # small delay to ensure different timestamps
        
        Post.objects.create(
            user=self.user1,
            title='User1 Post 2',
            content='Content 4'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('users:user-feed')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_info']['total_posts'], 2)
        
        # most recent post should be first
        self.assertEqual(response.data['posts'][0]['title'], 'User1 Post 2')


class UserIntegrationTests(APITestCase):
    """integration tests for user functionality"""
    
    def setUp(self):
        self.client = APIClient()
        # clean up any existing follows before each test
        Follow.objects.all().delete()
    
    def test_complete_user_workflow(self):
        """test complete user workflow from registration to posting"""
        # 1. Register user
        register_data = {
            'username': 'workflowuser',
            'email': 'workflow@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        register_response = self.client.post(reverse('users:user-register'), register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        token = register_response.data['token']
        
        # 2. Get user profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        profile_response = self.client.get(reverse('users:user-detail'))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        user_id = profile_response.data['id']
        
        # 3. Update profile
        update_data = {
            'bio': 'Test bio',
            'avatar': 'https://example.com/avatar.jpg'
        }
        update_response = self.client.patch(reverse('users:user-update'), update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # 4. Create a post (using posts API)
        post_data = {
            'username': 'workflowuser',
            'title': 'Test Post',
            'content': 'Test content'
        }
        post_response = self.client.post('/careers/create/', post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        
        # 5. Check user statistics
        stats_response = self.client.get(reverse('users:user-stats'))
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data['posts_count'], 1)
        
        # 6. Follow another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        follow_data = {'following': other_user.id}
        follow_response = self.client.post(reverse('users:follow-create'), follow_data)
        self.assertEqual(follow_response.status_code, status.HTTP_201_CREATED)
        
        # 7. Check following list
        following_response = self.client.get(reverse('users:follow-list'))
        self.assertEqual(following_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(following_response.data['results']), 1)
        
        # 8. Logout
        logout_response = self.client.post(reverse('users:user-logout'))
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
    
    def test_user_statistics_calculation(self):
        """test that user statistics are calculated correctly"""
        # create user
        user = User.objects.create_user(
            username='statsuser',
            email='stats@example.com',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # create followers
        follower1 = User.objects.create_user(
            username='follower1',
            email='follower1@example.com',
            password='testpass123'
        )
        follower2 = User.objects.create_user(
            username='follower2',
            email='follower2@example.com',
            password='testpass123'
        )
        Follow.objects.create(follower=follower1, following=user)
        Follow.objects.create(follower=follower2, following=user)
        
        # create following
        following_user = User.objects.create_user(
            username='followinguser',
            email='following@example.com',
            password='testpass123'
        )
        Follow.objects.create(follower=user, following=following_user)
        
        # create posts
        post1 = Post.objects.create(user=user, title='Post 1', content='Content 1')
        post2 = Post.objects.create(user=user, title='Post 2', content='Content 2')
        
        # create likes on posts
        Like.objects.create(user=follower1, post=post1)
        Like.objects.create(user=follower2, post=post1)
        Like.objects.create(user=follower1, post=post2)
        
        # create comments on posts
        Comment.objects.create(user=follower1, post=post1, content='Great post!')
        Comment.objects.create(user=follower2, post=post2, content='Awesome!')
        
        # check statistics
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(reverse('users:user-stats'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['posts_count'], 2)
        self.assertEqual(response.data['followers_count'], 2)
        self.assertEqual(response.data['following_count'], 1)
        self.assertEqual(response.data['likes_received'], 3)
        self.assertEqual(response.data['comments_received'], 2)
