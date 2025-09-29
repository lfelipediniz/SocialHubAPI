# Users API Documentation



## Base URL

http://localhost:8000/careers/users/



## Authentication mode (JWT)

- Use header: Authorization: Bearer <token>


- Access token expiry: 60 minutes


- Refresh token expiry: 7 days



## Common headers

- Content-Type: application/json



## Authentication endpoints



### Register user

POST /careers/users/register/


Body:
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Alice",
  "last_name": "Smith",
  "bio": "Software developer passionate about APIs"
}
````

Response 201:

```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "bio": "Software developer passionate about APIs",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

### Login

POST /careers/users/login/

Body:

```json
{ "username": "alice", "password": "password123" }
```

Response 200:

```json
{
  "user": { "id": 1, "username": "alice", "email": "alice@example.com", "first_name": "Alice", "last_name": "Smith" },
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

### Refresh token

POST /careers/users/token/refresh/

Body:

```json
{ "refresh": "REFRESH_TOKEN" }
```

Response 200:

```json
{ "access": "NEW_ACCESS_TOKEN" }
```

### Logout

POST /careers/users/logout/

Headers:
Authorization: Bearer <access_token>

Body:

```json
{ "refresh": "REFRESH_TOKEN" }
```

Response 200:

```json
{ "message": "Successfully logged out" }
```

## User management

### List users

GET /careers/users/?search=<q>&batch_size=10&batch_number=0

Notes:

* search: matches username, first_name, last_name, bio

* first_name: contains filter

* last_name: contains filter

* ordering: username or created_at or first_name or last_name

* batch_size: default 10, max 100

* batch_number: starts at 0

Response 200:

```json
{
  "message": "Users retrieved successfully",
  "users": [
    {
      "id": 1,
      "username": "alice",
      "first_name": "Alice",
      "last_name": "Smith",
      "avatar": "https://example.com/avatar.jpg",
      "is_following": false
    }
  ],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 10,
    "total_users": 25,
    "total_batches": 3,
    "users_in_current_batch": 10
  }
}
```

### Get user profile

GET /careers/users/{username}/

Response 200:

```json
{
  "id": 1,
  "username": "alice",
  "first_name": "Alice",
  "last_name": "Smith",
  "bio": "Software developer passionate about APIs",
  "avatar": "https://example.com/avatar.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "posts_count": 15,
  "followers_count": 42,
  "following_count": 28
}
```

### Get my profile

GET /careers/users/me/

Response 200:

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "bio": "Software developer passionate about APIs",
  "avatar": "https://example.com/avatar.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "posts_count": 15,
  "followers_count": 42,
  "following_count": 28
}
```

### Update my profile

PATCH /careers/users/me/update/

Body (any subset):

```json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "bio": "Updated bio",
  "avatar": "https://example.com/new-avatar.jpg",
  "email": "alice.johnson@example.com"
}
```

Response 200:

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice.johnson@example.com",
  "first_name": "Alice",
  "last_name": "Johnson",
  "bio": "Updated bio",
  "avatar": "https://example.com/new-avatar.jpg",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

## Social features

### Follow user

POST /careers/users/follow/

Headers:
Authorization: Bearer <access_token>

Body:

```json
{ "following": 2 }
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

Response 200:

```json
{ "message": "Stopped following bob" }
```

### Get my following

GET /careers/users/following/

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

## User statistics and feed pointers

### Get my statistics

GET /careers/users/me/stats/

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

### Feed pointers

* Use /users and /careers endpoints described in the Social Features and Posts docs to assemble a personalized feed in the client

* Typical pattern: fetch /users/me/following and then query posts for those usernames
