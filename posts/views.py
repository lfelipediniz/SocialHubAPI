from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import User, Post, Like, Comment, Share
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, LikeSerializer, CommentSerializer, ShareSerializer, PostShareSerializer


# ============================================================================
# REQUIRED BASIC ROUTES (from specification)
# ============================================================================

@api_view(['GET'])
def     post_list(request):
    # get /careers/ - list posts with optional batch system
    # parameters: batch_size (max posts per batch), batch_number (batch number, default 0)
    posts = Post.objects.all().order_by('-created_datetime')  # newest first
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        posts = posts[start_index:end_index]
        
        # calculate total posts for response info
        total_posts = Post.objects.count()
        total_batches = (total_posts + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = PostSerializer(posts, many=True)
        return Response({
            'message': 'Posts retrieved successfully',
            'posts': serializer.data,
            'batch_info': {
                'current_batch': batch_number,
                'batch_size': batch_size,
                'total_posts': total_posts,
                'total_batches': total_batches,
                'posts_in_current_batch': len(serializer.data)
            }
        })
    else:
        # return all posts without batching
        serializer = PostSerializer(posts, many=True)
        return Response({
            'message': 'All posts retrieved successfully',
            'posts': serializer.data,
            'total_posts': posts.count()
        })


@api_view(['POST'])
def post_create(request):
    # post /careers/create/ - create post
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        response_serializer = PostSerializer(post)
        return Response({
            'message': 'Post created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Post creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, pk):
    # get /careers/{id}/ - retrieve post, patch /careers/{id}/ - update post, delete /careers/{id}/ - delete post
    # supports three operations: GET (retrieve), PATCH (update), DELETE (remove)
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response({
            'message': 'Post retrieved successfully',
            'data': serializer.data
        })
    
    elif request.method == 'PATCH':
        # check authorization via x-username header
        username_header = request.META.get('HTTP_X_USERNAME')
        if not username_header or username_header != post.user.username:
            return Response(
                {'message': 'Access denied - X-Username header required and must match post author'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = PostSerializer(post)
            return Response({
                'message': 'Post updated successfully',
                'data': response_serializer.data
            })
        return Response({
            'message': 'Post update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # check authorization via x-username header
        username_header = request.META.get('HTTP_X_USERNAME')
        if not username_header or username_header != post.user.username:
            return Response(
                {'message': 'Access denied - X-Username header required and must match post author'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.delete()
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# ADDITIONAL SOCIAL INTERACTION ROUTES - LIKES (my implementation)
# ============================================================================

@api_view(['POST'])
def post_like(request, post_id):
    # post /careers/{id}/like/ - like a post
    post = get_object_or_404(Post, pk=post_id)
    username = request.data.get('username')
    
    if not username:
        return Response(
            {'message': 'Username is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user, created = User.objects.get_or_create(username=username)
        like, created = Like.objects.get_or_create(
            post=post, 
            user=user
        )
        if created:
            serializer = LikeSerializer(like)
            return Response({
                'message': 'Post liked successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'Post already liked by this user'}, 
                status=status.HTTP_200_OK
            )
    except IntegrityError:
        return Response(
            {'message': 'Post already liked by this user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def post_unlike(request, post_id):
    # delete /careers/{id}/unlike/ - unlike a post
    post = get_object_or_404(Post, pk=post_id)
    username = request.data.get('username')
    
    if not username:
        return Response(
            {'message': 'Username is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(username=username)
        like = Like.objects.get(post=post, user=user)
        like.delete()
        return Response({
            'message': 'Post unliked successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    except (Like.DoesNotExist, User.DoesNotExist):
        return Response(
            {'message': 'Post not liked by this user'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def post_likes_list(request, post_id):
    # get /careers/{id}/likes/ - list all likes for a post
    post = get_object_or_404(Post, pk=post_id)
    likes = post.likes.all()
    serializer = LikeSerializer(likes, many=True)
    return Response({
        'message': 'Likes retrieved successfully',
        'data': serializer.data
    })


# ============================================================================
# ADDITIONAL SOCIAL INTERACTION ROUTES - COMMENTS (my implementation)
# ============================================================================

@api_view(['POST'])
def post_comment(request, post_id):
    # post /careers/{id}/comment/ - add comment to a post
    post = get_object_or_404(Post, pk=post_id)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(post=post)
        return Response({
            'message': 'Comment added successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Comment creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_comments_list(request, post_id):
    # get /careers/{id}/comments/ - list all comments for a post
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response({
        'message': 'Comments retrieved successfully',
        'data': serializer.data
    })


# ============================================================================
# ADDITIONAL SOCIAL INTERACTION ROUTES - SHARES (my implementation)
# ============================================================================

@api_view(['POST'])
def post_share(request, post_id):
    # post /careers/{id}/share/ - share a post
    post = get_object_or_404(Post, pk=post_id)
    username = request.data.get('username')
    
    if not username:
        return Response(
            {'message': 'Username is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user, created = User.objects.get_or_create(username=username)
        share, created = Share.objects.get_or_create(
            post=post, 
            user=user
        )
        if created:
            serializer = ShareSerializer(share)
            return Response({
                'message': 'Post shared successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'Post already shared by this user'}, 
                status=status.HTTP_200_OK
            )
    except IntegrityError:
        return Response(
            {'message': 'Post already shared by this user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def post_shares_list(request, post_id):
    # get /careers/{id}/shares/ - list all shares for a post
    post = get_object_or_404(Post, pk=post_id)
    shares = post.share_actions.all()
    serializer = ShareSerializer(shares, many=True)
    return Response({
        'message': 'Shares retrieved successfully',
        'data': serializer.data
    })


# ============================================================================
# POST SHARING SYSTEM (new implementation)
# ============================================================================

@api_view(['POST'])
def post_share_create(request, post_id):
    # post /careers/{id}/share-post/ - create a new shared post
    original_post = get_object_or_404(Post, pk=post_id)
    
    # prevent sharing chains - always point to the original post
    if original_post.post_type == 'shared' and original_post.original_post:
        original_post = original_post.original_post
    
    serializer = PostShareSerializer(data=request.data)
    if serializer.is_valid():
        # get or create user
        username = serializer.validated_data['username']
        user, created = User.objects.get_or_create(username=username)
        
        # create the shared post
        shared_post = Post.objects.create(
            user=user,
            title=f"Shared: {original_post.title}",
            content=original_post.content,
            post_type='shared',
            original_post=original_post,
            share_comment=serializer.validated_data.get('share_comment', '')
        )
        
        # increment share count on original post
        # (this will be handled by the shares_count property)
        
        response_serializer = PostSerializer(shared_post)
        return Response({
            'message': 'Post shared successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'message': 'Post sharing failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)