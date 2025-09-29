from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Post, Like, Comment, Share
from django.conf import settings
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, LikeSerializer, CommentSerializer, ShareSerializer, PostShareSerializer
from users.models import User


# ============================================================================
# REQUIRED BASIC ROUTES (from specification)
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
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
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
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
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'message': 'All posts retrieved successfully',
            'posts': serializer.data,
            'total_posts': posts.count()
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_create(request):
    # post /careers/create/ - create post
    serializer = PostCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        post = serializer.save()
        response_serializer = PostSerializer(post, context={'request': request})
        return Response({
            'message': 'Post created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Falha ao criar post. Verifique os erros abaixo:',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.AllowAny])
def post_detail(request, pk):
    # get /careers/{id}/ - retrieve post, patch /careers/{id}/ - update post, delete /careers/{id}/ - delete post
    # supports three operations: GET (retrieve), PATCH (update), DELETE (remove)
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response({
            'message': 'Post retrieved successfully',
            'data': serializer.data
        })
    
    elif request.method == 'PATCH':
        # check authorization with JWT authentication
        if not request.user.is_authenticated:
            return Response(
                {'message': 'Authentication required - JWT token must be provided'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.user != post.user:
            return Response(
                {'message': 'Access denied - You can only edit your own posts'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = PostSerializer(post, context={'request': request})
            return Response({
                'message': 'Post updated successfully',
                'data': response_serializer.data
            })
        return Response({
            'message': 'Falha ao atualizar post. Verifique os erros abaixo:',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # check authorization with JWT authentication
        if not request.user.is_authenticated:
            return Response(
                {'message': 'Authentication required - JWT token must be provided'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.user != post.user:
            return Response(
                {'message': 'Access denied - You can only delete your own posts'}, 
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
@permission_classes([permissions.IsAuthenticated])
def post_like(request, post_id):
    # post /careers/{id}/like/ - like a post
    post = get_object_or_404(Post, pk=post_id)
    
    try:
        like, created = Like.objects.get_or_create(
            post=post, 
            user=request.user
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
@permission_classes([permissions.IsAuthenticated])
def post_unlike(request, post_id):
    # delete /careers/{id}/unlike/ - unlike a post
    post = get_object_or_404(Post, pk=post_id)
    
    try:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        return Response({
            'message': 'Post unliked successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response(
            {'message': 'Post not liked by this user'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def post_likes_list(request, post_id):
    # get /careers/{id}/likes/ - list all likes for a post with optional batch system
    # parameters: batch_size (max likes per batch), batch_number (batch number, default 0)
    post = get_object_or_404(Post, pk=post_id)
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        likes = post.likes.all()[start_index:end_index]
        
        # calculate total likes for response info
        total_likes = post.likes.count()
        total_batches = (total_likes + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = LikeSerializer(likes, many=True)
        return Response({
            'message': 'Likes retrieved successfully',
            'likes': serializer.data,
            'batch_info': {
                'current_batch': batch_number,
                'batch_size': batch_size,
                'total_likes': total_likes,
                'total_batches': total_batches,
                'likes_in_current_batch': len(serializer.data)
            }
        })
    else:
        # return all likes without batching
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response({
            'message': 'All likes retrieved successfully',
            'likes': serializer.data,
            'total_likes': likes.count()
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_liked_posts(request, username):
    # get /careers/user/{username}/liked-posts/ - list all posts liked by a specific user
    # parameters: batch_size (max posts per batch), batch_number (batch number, default 0)
    from users.models import User
    user = get_object_or_404(User, username=username)
    
    # get posts liked by this user
    liked_posts = Post.objects.filter(likes__user=user).distinct().order_by('-created_datetime')
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        posts = liked_posts[start_index:end_index]
        
        # calculate total posts for response info
        total_posts = liked_posts.count()
        total_batches = (total_posts + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'message': f'Posts liked by {username} retrieved successfully',
            'username': username,
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
        # return all liked posts without batching
        serializer = PostSerializer(liked_posts, many=True, context={'request': request})
        return Response({
            'message': f'All posts liked by {username} retrieved successfully',
            'username': username,
            'posts': serializer.data,
            'total_posts': liked_posts.count()
        })


# ============================================================================
# ADDITIONAL SOCIAL INTERACTION ROUTES - COMMENTS (my implementation)
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_comment(request, post_id):
    # post /careers/{id}/comment/ - add comment to a post
    post = get_object_or_404(Post, pk=post_id)
    
    # get username from header or request data
    username = request.headers.get('X-Username') or request.data.get('user')
    if not username:
        return Response({
            'message': 'Falha ao criar comentário. Verifique os erros abaixo:',
            'errors': {'user': ['Username is required. Provide X-Username header or user in request body.']}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # add username to request data
    data = request.data.copy()
    data['user'] = username
    
    serializer = CommentSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(post=post)
        return Response({
            'message': 'Comment added successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Falha ao criar comentário. Verifique os erros abaixo:',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def post_comments_list(request, post_id):
    # get /careers/{id}/comments/ - list all comments for a post with optional batch system
    # parameters: batch_size (max comments per batch), batch_number (batch number, default 0)
    post = get_object_or_404(Post, pk=post_id)
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        comments = post.comments.all()[start_index:end_index]
        
        # calculate total comments for response info
        total_comments = post.comments.count()
        total_batches = (total_comments + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'message': 'Comments retrieved successfully',
            'comments': serializer.data,
            'batch_info': {
                'current_batch': batch_number,
                'batch_size': batch_size,
                'total_comments': total_comments,
                'total_batches': total_batches,
                'comments_in_current_batch': len(serializer.data)
            }
        })
    else:
        # return all comments without batching
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'message': 'All comments retrieved successfully',
            'comments': serializer.data,
            'total_comments': comments.count()
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
        from users.models import User
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
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
@permission_classes([permissions.AllowAny])
def post_shares_list(request, post_id):
    # get /careers/{id}/shares/ - list all shares for a post with optional batch system
    # parameters: batch_size (max shares per batch), batch_number (batch number, default 0)
    post = get_object_or_404(Post, pk=post_id)
    
    # get batch parameters
    batch_size = request.query_params.get('batch_size', None)
    batch_number = int(request.query_params.get('batch_number', 0))
    
    if batch_size:
        # apply batch system
        batch_size = int(batch_size)
        start_index = max(0, batch_number * batch_size)  # prevent negative indexing
        end_index = start_index + batch_size
        
        shares = post.share_actions.all()[start_index:end_index]
        
        # calculate total shares for response info
        total_shares = post.share_actions.count()
        total_batches = (total_shares + batch_size - 1) // batch_size if batch_size > 0 else 0  # ceiling division
        
        serializer = ShareSerializer(shares, many=True)
        return Response({
            'message': 'Shares retrieved successfully',
            'shares': serializer.data,
            'batch_info': {
                'current_batch': batch_number,
                'batch_size': batch_size,
                'total_shares': total_shares,
                'total_batches': total_batches,
                'shares_in_current_batch': len(serializer.data)
            }
        })
    else:
        # return all shares without batching
        shares = post.share_actions.all()
        serializer = ShareSerializer(shares, many=True)
        return Response({
            'message': 'All shares retrieved successfully',
            'shares': serializer.data,
            'total_shares': shares.count()
        })


# ============================================================================
# POST SHARING SYSTEM (new implementation)
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
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
        from users.models import User
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        
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
        
        response_serializer = PostSerializer(shared_post, context={'request': request})
        return Response({
            'message': 'Post shared successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
            'message': 'Falha ao compartilhar post. Verifique os erros abaixo:',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_shared_posts(request, username):
    """
    view for getting posts shared by a specific user
    """
    try:
        user = User.objects.get(username=username)
        
        # get batch parameters
        batch_size = request.query_params.get('batch_size', None)
        batch_number = int(request.query_params.get('batch_number', 0))
        
        # get posts shared by this user
        shared_posts = Post.objects.filter(share_actions__user=user).distinct()
        
        if batch_size:
            # apply batch system
            batch_size = int(batch_size)
            start_index = max(0, batch_number * batch_size)
            end_index = start_index + batch_size
            
            posts_batch = shared_posts[start_index:end_index]
            total_posts = shared_posts.count()
            total_batches = (total_posts + batch_size - 1) // batch_size
            
            serializer = PostSerializer(posts_batch, many=True, context={'request': request})
            
            return Response({
                'message': f'Posts compartilhados por {username} (lote {batch_number + 1} de {total_batches})',
                'count': total_posts,
                'next': f'?batch_size={batch_size}&batch_number={batch_number + 1}' if end_index < total_posts else None,
                'previous': f'?batch_size={batch_size}&batch_number={batch_number - 1}' if batch_number > 0 else None,
                'results': serializer.data,
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
            serializer = PostSerializer(shared_posts, many=True, context={'request': request})
            return Response({
                'message': f'Todos os posts compartilhados por {username}',
                'posts': serializer.data,
                'total_posts': shared_posts.count()
            })
            
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )