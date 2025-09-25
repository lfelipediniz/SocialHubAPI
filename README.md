# CodeLeap Careers API

A minimal public API that mirrors the behavior of `https://dev.codeleap.co.uk/careers/` with additional social interaction features.

## Base URL

```
http://localhost:8000/careers/
```

## Authentication

For write operations (UPDATE/DELETE), include the `X-Username` header:
```
X-Username: <username>
```

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

## Response Format

Posts include automatic counters:
```json
{
  "id": 1,
  "username": "user123",
  "title": "Post Title",
  "content": "Post content...",
  "created_datetime": "2025-09-25T14:07:19.904045Z",
  "likes_count": 5,
  "comments_count": 3,
  "shares_count": 2
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

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

## Features

- ✅ Full CRUD operations for posts
- ✅ Authorization via X-Username header
- ✅ Social interactions (likes, comments, shares)
- ✅ Batch pagination system
- ✅ Automatic post counters
- ✅ Partial updates (PATCH)
- ✅ Duplicate prevention for likes/shares