# SocialHubAPI

A comprehensive social media API with CRUD operations for posts and social interactions including likes, comments, and shares. Features unique username system and advanced post sharing capabilities.

## Base URL

```
http://localhost:8000/careers/
```

## Authentication

For write operations (UPDATE/DELETE), include the `X-Username` header:
```
X-Username: <username>
```

## User System

- **Unique Usernames**: Each username can only be used once across the entire system
- **Automatic User Creation**: Users are created automatically when first posting
- **User Reuse**: Same username reuses existing user account

## API Endpoints

### Basic Routes

#### 1. List Posts
- **GET** `/careers/`
- **Parameters (optional):**
  - `batch_size`: Max posts per batch
  - `batch_number`: Batch number (default: 0)
- **Response:** List of posts ordered by newest first

#### 2. Create Post
- **POST** `/careers/create/`
- **Body:**
  ```json
  {
    "username": "string",
    "title": "string",
    "content": "string"
  }
  ```
- **Response:** 201 with created post including `id` and `created_datetime`

#### 3. Get Post
- **GET** `/careers/{id}/`
- **Response:** Single post details

#### 4. Update Post
- **PATCH** `/careers/{id}/`
- **Headers:** `X-Username: <username>` (must match post author)
- **Body:**
  ```json
  {
    "title": "string",
    "content": "string"
  }
  ```
- **Note:** Only send fields you want to update

#### 5. Delete Post
- **DELETE** `/careers/{id}/`
- **Headers:** `X-Username: <username>` (must match post author)
- **Response:** 204 No Content

### Social Interaction Routes

#### Likes
- **POST** `/careers/{id}/like/` - Like a post
  ```json
  {"username": "string"}
  ```
- **DELETE** `/careers/{id}/unlike/` - Unlike a post
  ```json
  {"username": "string"}
  ```
- **GET** `/careers/{id}/likes/` - List all likes

#### Comments
- **POST** `/careers/{id}/comment/` - Add comment
  ```json
  {
    "username": "string",
    "content": "string"
  }
  ```
- **GET** `/careers/{id}/comments/` - List all comments

#### Shares
- **POST** `/careers/{id}/share/` - Share a post
  ```json
  {"username": "string"}
  ```
- **GET** `/careers/{id}/shares/` - List all shares

#### Post Sharing (New)
- **POST** `/careers/{id}/share-post/` - Create a new shared post
  ```json
  {
    "username": "string",
    "share_comment": "string (optional)"
  }
  ```

## Response Format

### Standard Post Response
Posts include automatic counters and metadata:
```json
{
  "id": 1,
  "username": "user123",
  "title": "Post Title",
  "content": "Post content...",
  "post_type": "original",
  "original_post": null,
  "share_comment": "",
  "created_datetime": "2025-09-25T14:07:19.904045Z",
  "likes_count": 5,
  "comments_count": 3,
  "shares_count": 2,
  "original_author": "user123",
  "original_content": "Post content...",
  "original_title": "Post Title"
}
```

### Shared Post Response
```json
{
  "id": 5,
  "username": "maria_shared",
  "title": "Shared: Original Post Title",
  "content": "Original post content...",
  "post_type": "shared",
  "original_post": 1,
  "share_comment": "My comment about this post",
  "created_datetime": "2025-09-25T15:30:00.000000Z",
  "likes_count": 0,
  "comments_count": 0,
  "shares_count": 0,
  "original_author": "original_author",
  "original_content": "Original post content...",
  "original_title": "Original Post Title"
}
```

### API Response Structure
All API responses include a `message` field:
```json
{
  "message": "Operation completed successfully",
  "data": { /* response data */ }
}
```

## Batch System

Use `batch_size` and `batch_number` parameters for pagination:

```bash
# Get first 5 posts (batch 0)
GET /careers/?batch_size=5&batch_number=0

# Get next 5 posts (batch 1)
GET /careers/?batch_size=5&batch_number=1
```

Response includes batch information:
```json
{
  "posts": [...],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 5,
    "total_posts": 20,
    "total_batches": 4,
    "posts_in_current_batch": 5
  }
}
```

## Status Codes

- **200** OK - Successful GET/PATCH
- **201** Created - Successful POST
- **204** No Content - Successful DELETE
- **400** Bad Request - Validation errors
- **403** Forbidden - Invalid X-Username header
- **404** Not Found - Post not found

## Usage Examples

### Creating and Managing Posts

```bash
# Create a new post
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "title": "My First Post",
    "content": "Hello, SocialHubAPI!"
  }'

# List all posts
curl -X GET "http://localhost:8000/careers/"

# List posts with pagination
curl -X GET "http://localhost:8000/careers/?batch_size=5&batch_number=0"

# Get specific post
curl -X GET "http://localhost:8000/careers/1/"

# Update post (requires X-Username header)
curl -X PATCH "http://localhost:8000/careers/1/" \
  -H "Content-Type: application/json" \
  -H "X-Username: john_doe" \
  -d '{"title": "Updated Title"}'

# Delete post (requires X-Username header)
curl -X DELETE "http://localhost:8000/careers/1/" \
  -H "X-Username: john_doe"
```

### Social Interactions

```bash
# Like a post
curl -X POST "http://localhost:8000/careers/1/like/" \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith"}'

# Add a comment
curl -X POST "http://localhost:8000/careers/1/comment/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_smith",
    "content": "Great post!"
  }'

# Share a post
curl -X POST "http://localhost:8000/careers/1/share/" \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith"}'

# Create a shared post with comment
curl -X POST "http://localhost:8000/careers/1/share-post/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_smith",
    "share_comment": "This is amazing! Everyone should see this."
  }'
```

### Viewing Interactions

#### Get Post Details (with counters)
```bash
# Get post with automatic counters (likes_count, comments_count, shares_count)
curl -X GET "http://localhost:8000/careers/1/"
```
**Response includes:**
- Post details
- `likes_count`: Total number of likes
- `comments_count`: Total number of comments  
- `shares_count`: Total number of shares

#### List Individual Interactions
```bash
# List all users who liked the post (with usernames and timestamps)
curl -X GET "http://localhost:8000/careers/1/likes/"

# List all comments for a post (with usernames, content, and timestamps)
curl -X GET "http://localhost:8000/careers/1/comments/"

# List all users who shared the post (with usernames and timestamps)
curl -X GET "http://localhost:8000/careers/1/shares/"
```

**Example Response for `/likes/`:**
```json
{
  "message": "Likes retrieved successfully",
  "data": [
    {
      "id": 5,
      "username": "bob",
      "created_datetime": "2025-09-25T17:30:07.874599Z"
    },
    {
      "id": 4,
      "username": "alice", 
      "created_datetime": "2025-09-25T17:30:01.125244Z"
    }
  ]
}
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

## User Management System

### Unique Username System
- **One Username Per System**: Each username can only be used once across the entire API
- **Automatic User Creation**: Users are created automatically when they first post
- **User Reuse**: Subsequent posts with the same username reuse the existing user account
- **Database Integrity**: Username uniqueness is enforced at the database level

### User Creation Flow
1. **First Post**: When a new username is used, a new user is automatically created
2. **Subsequent Posts**: Same username reuses the existing user account
3. **Social Interactions**: All likes, comments, and shares are linked to the user account

### Example User Creation
```bash
# First post with username "alice" - creates new user
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "title": "Alice First Post",
    "content": "Hello from Alice!"
  }'

# Second post with same username - reuses existing user
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "title": "Alice Second Post", 
    "content": "Another post from Alice!"
  }'
```

## Post Sharing System

The API includes a comprehensive post sharing system:

### How it works:
1. **Create Shared Post**: Use `/careers/{id}/share-post/` to create a new post that shares another post
2. **Chain Prevention**: If you share a post that's already shared, it points directly to the original post
3. **Share Comments**: Add your own comment when sharing a post
4. **Automatic Counters**: Original posts track how many times they've been shared

### Shared Post Structure:
```json
{
  "id": 5,
  "username": "maria_shared",
  "title": "Shared: Original Post Title",
  "content": "Original post content...",
  "post_type": "shared",
  "original_post": 1,
  "share_comment": "My comment about this post",
  "original_author": "original_author",
  "original_content": "Original post content...",
  "original_title": "Original Post Title"
}
```

## Testing

The API includes comprehensive test coverage with 44 test cases:

```bash
# Run all tests
python manage.py test posts.tests

# Run specific test categories
python manage.py test posts.tests.UserModelTest
python manage.py test posts.tests.PostAPITest
python manage.py test posts.tests.LikeAPITest
python manage.py test posts.tests.CommentAPITest
python manage.py test posts.tests.ShareAPITest
python manage.py test posts.tests.PostSharingAPITest
python manage.py test posts.tests.EdgeCasesTest
```

### Test Coverage
- ✅ **Model Tests**: User creation, uniqueness, post properties
- ✅ **API Tests**: All CRUD operations and social interactions
- ✅ **Edge Cases**: Invalid data, concurrent operations, unicode content
- ✅ **Validation**: Field validation and error handling
- ✅ **Authorization**: X-Username header validation
- ✅ **Batch System**: Pagination with various parameters

## Features

- ✅ **Unique Username System**: Each username can only be used once
- ✅ **Full CRUD Operations**: Complete post management
- ✅ **Social Interactions**: Likes, comments, and shares
- ✅ **Advanced Post Sharing**: Chain prevention and share comments
- ✅ **Batch Pagination**: Efficient data loading
- ✅ **Automatic Counters**: Real-time interaction counts
- ✅ **Partial Updates**: PATCH with field validation
- ✅ **Duplicate Prevention**: Unique constraints for interactions
- ✅ **Comprehensive Testing**: 44 test cases with 100% pass rate
- ✅ **Error Handling**: Detailed error messages and status codes
- ✅ **Unicode Support**: Full international character support