# Social Features API 



## Base URLs

Posts: http://localhost:8000/careers/

User: http://localhost:8000/careers/users/



## Required headers

Authorization: Bearer <token>

Content-Type: application/json



## Pagination (batch system)

- batch_size: default 10, max 100


- batch_number: starts at 0



## Post interactions



### Likes

#### Like a post

POST /careers/{id}/like/


Example:
```bash
curl -X POST "http://localhost:8000/careers/1/like/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 201:

```json
{ "message": "Post liked successfully" }
```

#### Unlike a post

DELETE /careers/{id}/unlike/

Example:

```bash
curl -X DELETE "http://localhost:8000/careers/1/unlike/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 204: empty body

#### List likes

GET /careers/{id}/likes/?batch_size=10&batch_number=0

Example:

```bash
curl -X GET "http://localhost:8000/careers/1/likes/?batch_size=10&batch_number=0" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "message": "Likes retrieved successfully",
  "likes": [
    { "id": 1, "user": "alice", "created_at": "2024-01-15T10:30:00Z" }
  ],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 10,
    "total_likes": 25,
    "total_batches": 3,
    "likes_in_current_batch": 10
  }
}
```

### Comments

#### Add comment

POST /careers/{id}/comment/

Body:

```json
{ "content": "This is a great post!" }
```

Example:

```bash
curl -X POST "http://localhost:8000/careers/1/comment/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"This is a great post!"}'
```

Response 201:

```json
{
  "id": 1,
  "user": "alice",
  "content": "This is a great post!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List comments

GET /careers/{id}/comments/?batch_size=10&batch_number=0

Example:

```bash
curl -X GET "http://localhost:8000/careers/1/comments/?batch_size=10&batch_number=0" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "message": "Comments retrieved successfully",
  "comments": [
    { "id": 1, "user": "alice", "content": "This is a great post!", "created_at": "2024-01-15T10:30:00Z" }
  ],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 10,
    "total_comments": 15,
    "total_batches": 2,
    "comments_in_current_batch": 10
  }
}
```

### Shares

#### Share a post

POST /careers/{id}/share/

Example:

```bash
curl -X POST "http://localhost:8000/careers/1/share/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 201:

```json
{ "message": "Post shared successfully" }
```

#### List shares

GET /careers/{id}/shares/?batch_size=10&batch_number=0

Example:

```bash
curl -X GET "http://localhost:8000/careers/1/shares/?batch_size=10&batch_number=0" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "message": "Shares retrieved successfully",
  "shares": [
    { "id": 1, "user": "alice", "created_at": "2024-01-15T10:30:00Z" }
  ],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 10,
    "total_shares": 8,
    "total_batches": 1,
    "shares_in_current_batch": 8
  }
}
```

#### Create shared post

POST /careers/{id}/share-post/

Body:

```json
{ "title": "My thoughts on this post", "content": "I found this post really interesting because..." }
```

Example:

```bash
curl -X POST "http://localhost:8000/careers/1/share-post/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My thoughts on this post","content":"I found this post really interesting because..."}'
```

Response 201:

```json
{
  "id": 2,
  "username": "alice",
  "title": "My thoughts on this post",
  "content": "I found this post really interesting because...",
  "created_datetime": "2024-01-15T10:30:00Z",
  "original_post": 1,
  "post_type": "share"
}
```

## User relationships

### Follow user

POST /careers/users/follow/

Body:

```json
{ "following": 2 }
```

Example:

```bash
curl -X POST "http://localhost:8000/careers/users/follow/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"following": 2}'
```

Response 201:

```json
{
  "id": 1,
  "follower": 1,
  "following": 2,
  "follower_username": "alice",
  "following_username": "bob",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Unfollow user

DELETE /careers/users/{username}/unfollow/

Example:

```bash
curl -X DELETE "http://localhost:8000/careers/users/bob/unfollow/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{ "message": "Stopped following bob" }
```

### Get my following

GET /careers/users/following/

Example:

```bash
curl -X GET "http://localhost:8000/careers/users/following/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "follower": 1,
      "following": 2,
      "follower_username": "alice",
      "following_username": "bob",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get a user's followers

GET /careers/users/{username}/followers/

Example:

```bash
curl -X GET "http://localhost:8000/careers/users/alice/followers/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "username": "charlie",
      "first_name": "Charlie",
      "last_name": "Brown",
      "avatar": "https://example.com/avatar.jpg",
      "is_following": false
    }
  ]
}
```

### Get a user's following

GET /careers/users/{username}/following/

Example:

```bash
curl -X GET "http://localhost:8000/careers/users/alice/following/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "username": "david",
      "first_name": "David",
      "last_name": "Wilson",
      "avatar": "https://example.com/avatar.jpg",
      "is_following": true
    }
  ]
}
```

## Feed

### Personalized feed

GET /careers/users/me/feed/?batch_size=20&batch_number=0

Example:

```bash
curl -X GET "http://localhost:8000/careers/users/me/feed/?batch_size=20&batch_number=0" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "message": "Feed retrieved successfully",
  "posts": [
    { "id": 1, "username": "bob", "title": "New Post from Bob", "content": "Post body", "created_datetime": "2024-01-15T10:30:00Z" },
    { "id": 2, "username": "alice", "title": "My Own Post", "content": "Post body", "created_datetime": "2024-01-15T09:30:00Z" }
  ],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 20,
    "total_posts": 50,
    "total_batches": 3,
    "posts_in_current_batch": 20
  }
}
```

## User statistics

### Get my stats

GET /careers/users/me/stats/

Example:

```bash
curl -X GET "http://localhost:8000/careers/users/me/stats/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

Response 200:

```json
{
  "posts_count": 15,
  "followers_count": 42,
  "following_count": 28,
  "likes_received": 156,
  "comments_received": 89
}
```


