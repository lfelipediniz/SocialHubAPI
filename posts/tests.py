from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Post, Like, Comment, Share


class UserModelTest(TestCase):
    # test user model functionality
    
    def test_user_creation(self):
        # test basic user creation
        user = User.objects.create(username="testuser")
        self.assertEqual(user.username, "testuser")
        self.assertIsNotNone(user.created_datetime)
    
    def test_user_unique_username(self):
        # test username uniqueness constraint
        User.objects.create(username="uniqueuser")
        with self.assertRaises(Exception):
            User.objects.create(username="uniqueuser")
    
    def test_user_str_representation(self):
        # test user string representation
        user = User.objects.create(username="testuser")
        self.assertEqual(str(user), "testuser")


class PostModelTest(TestCase):
    # test post model functionality
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
    
    def test_post_creation(self):
        # test basic post creation
        post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.post_type, "original")
    
    def test_shared_post_creation(self):
        # test shared post creation
        original_post = Post.objects.create(
            user=self.user,
            title="Original Post",
            content="Original content"
        )
        shared_post = Post.objects.create(
            user=self.user,
            title="Shared: Original Post",
            content="Original content",
            post_type="shared",
            original_post=original_post,
            share_comment="Great post!"
        )
        self.assertEqual(shared_post.post_type, "shared")
        self.assertEqual(shared_post.original_post, original_post)
        self.assertEqual(shared_post.share_comment, "Great post!")
    
    def test_post_properties(self):
        # test post computed properties
        post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
        
        # test original_author property
        self.assertEqual(post.original_author, "testuser")
        
        # test original_content property
        self.assertEqual(post.original_content, "Test content")
        
        # test original_title property
        self.assertEqual(post.original_title, "Test Post")


class PostAPITest(APITestCase):
    # test post API endpoints
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
    
    def test_create_post(self):
        # test post creation via API
        url = reverse('post-create')
        data = {
            "username": "newuser",
            "title": "New Post",
            "content": "New content"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Post created successfully')
        self.assertEqual(response.data['data']['title'], 'New Post')
        self.assertEqual(response.data['data']['username'], 'newuser')
    
    def test_create_post_with_existing_username(self):
        # test post creation with existing username
        url = reverse('post-create')
        data = {
            "username": "testuser",  # existing username
            "title": "Another Post",
            "content": "Another content"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # should reuse existing user
        self.assertEqual(response.data['data']['username'], 'testuser')
    
    def test_create_post_validation_errors(self):
        # test post creation with validation errors
        url = reverse('post-create')
        
        # test empty title
        data = {
            "username": "testuser",
            "title": "",
            "content": "Test content"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Post creation failed')
        
        # test empty content
        data = {
            "username": "testuser",
            "title": "Test title",
            "content": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # test empty username
        data = {
            "username": "",
            "title": "Test title",
            "content": "Test content"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_posts(self):
        # test post listing
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'All posts retrieved successfully')
        self.assertGreater(len(response.data['posts']), 0)
    
    def test_list_posts_with_batch(self):
        # test post listing with batch system
        url = reverse('post-list')
        response = self.client.get(url, {'batch_size': 1, 'batch_number': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Posts retrieved successfully')
        self.assertIn('batch_info', response.data)
        self.assertEqual(response.data['batch_info']['batch_size'], 1)
        self.assertEqual(response.data['batch_info']['current_batch'], 0)
    
    def test_get_post_detail(self):
        # test get single post
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post retrieved successfully')
        self.assertEqual(response.data['data']['id'], self.post.id)
    
    def test_get_nonexistent_post(self):
        # test get nonexistent post
        url = reverse('post-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_post_without_authorization(self):
        # test update post without X-Username header
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Access denied', response.data['message'])
    
    def test_update_post_with_wrong_authorization(self):
        # test update post with wrong X-Username header
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json', HTTP_X_USERNAME='wronguser')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_post_with_correct_authorization(self):
        # test update post with correct X-Username header
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json', HTTP_X_USERNAME='testuser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post updated successfully')
        self.assertEqual(response.data['data']['title'], 'Updated Title')
    
    def test_partial_update_post(self):
        # test partial update (only title)
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {"title": "Only Title Updated"}
        response = self.client.patch(url, data, format='json', HTTP_X_USERNAME='testuser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # content should remain unchanged
        self.assertEqual(response.data['data']['content'], 'Test content')
    
    def test_delete_post_without_authorization(self):
        # test delete post without X-Username header
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_post_with_correct_authorization(self):
        # test delete post with correct X-Username header
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url, HTTP_X_USERNAME='testuser')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Post deleted successfully')
        
        # verify post is deleted
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


class LikeAPITest(APITestCase):
    # test like API endpoints
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
    
    def test_like_post(self):
        # test liking a post
        url = reverse('post-like', kwargs={'post_id': self.post.id})
        data = {"username": "liker"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Post liked successfully')
        
        # verify like was created
        self.assertTrue(Like.objects.filter(post=self.post, user__username='liker').exists())
    
    def test_like_post_duplicate(self):
        # test liking same post twice
        liker_user = User.objects.create(username="liker")
        Like.objects.create(post=self.post, user=liker_user)
        
        url = reverse('post-like', kwargs={'post_id': self.post.id})
        data = {"username": "liker"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post already liked by this user')
    
    def test_like_post_missing_username(self):
        # test liking post without username
        url = reverse('post-like', kwargs={'post_id': self.post.id})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Username is required')
    
    def test_unlike_post(self):
        # test unliking a post
        liker_user = User.objects.create(username="liker")
        Like.objects.create(post=self.post, user=liker_user)
        
        url = reverse('post-unlike', kwargs={'post_id': self.post.id})
        data = {"username": "liker"}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Post unliked successfully')
        
        # verify like was removed
        self.assertFalse(Like.objects.filter(post=self.post, user__username='liker').exists())
    
    def test_unlike_post_not_liked(self):
        # test unliking a post that wasn't liked
        url = reverse('post-unlike', kwargs={'post_id': self.post.id})
        data = {"username": "neverliked"}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Post not liked by this user')
    
    def test_list_post_likes(self):
        # test listing post likes
        liker1 = User.objects.create(username="liker1")
        liker2 = User.objects.create(username="liker2")
        Like.objects.create(post=self.post, user=liker1)
        Like.objects.create(post=self.post, user=liker2)
        
        url = reverse('post-likes-list', kwargs={'post_id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Likes retrieved successfully')
        self.assertEqual(len(response.data['data']), 2)


class CommentAPITest(APITestCase):
    # test comment API endpoints
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
    
    def test_comment_post(self):
        # test commenting on a post
        url = reverse('post-comment', kwargs={'post_id': self.post.id})
        data = {
            "username": "commenter",
            "content": "Great post!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Comment added successfully')
        
        # verify comment was created
        self.assertTrue(Comment.objects.filter(post=self.post, user__username='commenter').exists())
    
    def test_comment_post_validation_errors(self):
        # test commenting with validation errors
        url = reverse('post-comment', kwargs={'post_id': self.post.id})
        
        # test empty content
        data = {
            "username": "commenter",
            "content": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Comment creation failed')
        
        # test empty username
        data = {
            "username": "",
            "content": "Great post!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_post_comments(self):
        # test listing post comments
        commenter1 = User.objects.create(username="commenter1")
        commenter2 = User.objects.create(username="commenter2")
        Comment.objects.create(post=self.post, user=commenter1, content="First comment")
        Comment.objects.create(post=self.post, user=commenter2, content="Second comment")
        
        url = reverse('post-comments-list', kwargs={'post_id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Comments retrieved successfully')
        self.assertEqual(len(response.data['data']), 2)


class ShareAPITest(APITestCase):
    # test share API endpoints
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
    
    def test_share_post(self):
        # test sharing a post
        url = reverse('post-share', kwargs={'post_id': self.post.id})
        data = {"username": "sharer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Post shared successfully')
        
        # verify share was created
        self.assertTrue(Share.objects.filter(post=self.post, user__username='sharer').exists())
    
    def test_share_post_duplicate(self):
        # test sharing same post twice
        sharer_user = User.objects.create(username="sharer")
        Share.objects.create(post=self.post, user=sharer_user)
        
        url = reverse('post-share', kwargs={'post_id': self.post.id})
        data = {"username": "sharer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post already shared by this user')
    
    def test_list_post_shares(self):
        # test listing post shares
        sharer1 = User.objects.create(username="sharer1")
        sharer2 = User.objects.create(username="sharer2")
        Share.objects.create(post=self.post, user=sharer1)
        Share.objects.create(post=self.post, user=sharer2)
        
        url = reverse('post-shares-list', kwargs={'post_id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Shares retrieved successfully')
        self.assertEqual(len(response.data['data']), 2)


class PostSharingAPITest(APITestCase):
    # test post sharing system (new implementation)
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Original Post",
            content="Original content"
        )
    
    def test_share_post_create(self):
        # test creating a shared post
        url = reverse('post-share-create', kwargs={'post_id': self.post.id})
        data = {
            "username": "sharer",
            "share_comment": "This is amazing!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Post shared successfully')
        
        # verify shared post was created
        shared_post = Post.objects.filter(post_type='shared', original_post=self.post).first()
        self.assertIsNotNone(shared_post)
        self.assertEqual(shared_post.user.username, 'sharer')
        self.assertEqual(shared_post.share_comment, 'This is amazing!')
        self.assertEqual(shared_post.title, 'Shared: Original Post')
    
    def test_share_post_without_comment(self):
        # test creating a shared post without comment
        url = reverse('post-share-create', kwargs={'post_id': self.post.id})
        data = {"username": "sharer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # verify shared post was created without comment
        shared_post = Post.objects.filter(post_type='shared', original_post=self.post).first()
        self.assertEqual(shared_post.share_comment, '')
    
    def test_share_shared_post_chain_prevention(self):
        # test sharing a shared post (chain prevention)
        # first create a shared post
        sharer1 = User.objects.create(username="sharer1")
        shared_post = Post.objects.create(
            user=sharer1,
            title="Shared: Original Post",
            content="Original content",
            post_type="shared",
            original_post=self.post,
            share_comment="First share"
        )
        
        # now share the shared post
        url = reverse('post-share-create', kwargs={'post_id': shared_post.id})
        data = {
            "username": "sharer2",
            "share_comment": "Second share"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # verify new shared post points to original post, not the intermediate shared post
        new_shared_post = Post.objects.filter(
            post_type='shared', 
            user__username='sharer2'
        ).first()
        self.assertEqual(new_shared_post.original_post, self.post)
        self.assertNotEqual(new_shared_post.original_post, shared_post)
    
    def test_share_post_validation_errors(self):
        # test sharing post with validation errors
        url = reverse('post-share-create', kwargs={'post_id': self.post.id})
        
        # test empty username
        data = {
            "username": "",
            "share_comment": "Great post!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Post sharing failed')
    
    def test_share_nonexistent_post(self):
        # test sharing nonexistent post
        url = reverse('post-share-create', kwargs={'post_id': 99999})
        data = {
            "username": "sharer",
            "share_comment": "Great post!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EdgeCasesTest(APITestCase):
    # test edge cases and error scenarios
    
    def setUp(self):
        # setup test data
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content"
        )
    
    def test_empty_batch_parameters(self):
        # test batch system with edge cases
        url = reverse('post-list')
        
        # test with batch_size=0
        response = self.client.get(url, {'batch_size': 0, 'batch_number': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # test with negative batch_number
        response = self.client.get(url, {'batch_size': 1, 'batch_number': -1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_large_batch_number(self):
        # test batch system with large batch number
        url = reverse('post-list')
        response = self.client.get(url, {'batch_size': 1, 'batch_number': 99999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return empty results
        self.assertEqual(len(response.data['posts']), 0)
    
    def test_username_with_special_characters(self):
        # test username with special characters
        url = reverse('post-create')
        data = {
            "username": "user@domain.com",
            "title": "Test Post",
            "content": "Test content"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_very_long_content(self):
        # test post with very long content
        url = reverse('post-create')
        long_content = "A" * 10000  # 10k characters
        data = {
            "username": "testuser",
            "title": "Long Post",
            "content": long_content
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unicode_content(self):
        # test post with unicode content
        url = reverse('post-create')
        unicode_content = "Test with émojis 🚀 and ñ characters"
        data = {
            "username": "testuser",
            "title": "Unicode Post",
            "content": unicode_content
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['content'], unicode_content)
    
    def test_concurrent_likes(self):
        # test concurrent likes from same user
        url = reverse('post-like', kwargs={'post_id': self.post.id})
        data = {"username": "concurrent_user"}
        
        # simulate concurrent requests
        response1 = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        
        # first should succeed, second should return already liked
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # verify only one like exists
        self.assertEqual(Like.objects.filter(post=self.post, user__username='concurrent_user').count(), 1)
    
    def test_cascade_deletion(self):
        # test cascade deletion when user is deleted
        user = User.objects.create(username="tobedeleted")
        post = Post.objects.create(user=user, title="Test", content="Test")
        like = Like.objects.create(post=post, user=user)
        comment = Comment.objects.create(post=post, user=user, content="Test comment")
        share = Share.objects.create(post=post, user=user)
        
        # delete user
        user.delete()
        
        # verify cascade deletion
        self.assertFalse(Post.objects.filter(id=post.id).exists())
        self.assertFalse(Like.objects.filter(id=like.id).exists())
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        self.assertFalse(Share.objects.filter(id=share.id).exists())
    
    def test_post_counters_accuracy(self):
        # test that post counters are accurate
        liker = User.objects.create(username="liker")
        commenter = User.objects.create(username="commenter")
        sharer = User.objects.create(username="sharer")
        
        # add interactions
        Like.objects.create(post=self.post, user=liker)
        Comment.objects.create(post=self.post, user=commenter, content="Test comment")
        Share.objects.create(post=self.post, user=sharer)
        
        # refresh post from database
        self.post.refresh_from_db()
        
        # test counters
        self.assertEqual(self.post.likes_count, 1)
        self.assertEqual(self.post.comments_count, 1)
        self.assertEqual(self.post.shares_count, 1)
