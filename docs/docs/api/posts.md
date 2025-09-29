# Posts API Documentation 



## Base URL

http://localhost:8000/careers/



## Required Headers

Authorization: Bearer <token>

Content-Type: application/json



## Pagination (used on list endpoints)

- `batch_size`: default 10, max 100


- `batch_number`: default 0



## Field limits

- Post `title`: required, max 200 chars


- Post `content`: required, max 5000 chars


- Comment `content`: required, max 1000 chars


## Quick model shapes

* Post:
  ```json
  { "id": 1, "username": "alice", "title": "Hello", "content": "Body", "created_datetime": "2024-01-15T10:30:00Z", "post_type": "post", "original_post": null }
  ```

* Like:
  ```json
  { "id": 10, "post": 1, "user": 2, "username": "alice", "created_datetime": "2024-01-15T10:30:00Z" }
  ```

* Comment:
  ```json
  { "id": 7, "post": 1, "user": 2, "username": "alice", "content": "Great post!", "created_datetime": "2024-01-15T10:30:00Z" }
  ```

## Core flow (CRUD)

### 1) Create post

POST `/careers/create/`

Body:
```json
{ "username": "alice", "title": "My Post", "content": "This is the content" }
```

Example:
```bash
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","title":"My Post","content":"This is the content"}'
```

Response: `201 Created` (returns the created post)

### 2) List posts

GET `/careers/`

Example:
```bash
curl -X GET "http://localhost:8000/careers/?batch_size=10&batch_number=0" \
  -H "Authorization: Bearer <token>"
```

Response: `200 OK` with pagination wrapper

### 3) Retrieve a post

GET `/careers/{id}/`

Example:
```bash
curl -X GET "http://localhost:8000/careers/1/" \
  -H "Authorization: Bearer <token>"
```

Response: `200 OK` with the post object

### 4) Update a post

PATCH `/careers/{id}/`

Body (one or both fields):
```json
{ "title": "New title", "content": "New content" }
```

Example:
```bash
curl -X PATCH "http://localhost:8000/careers/1/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New title","content":"New content"}'
```

Response: `200 OK` with the updated post

### 5) Delete a post

DELETE `/careers/{id}/`

Example:

```bash
curl -X DELETE "http://localhost:8000/careers/1/" \
  -H "Authorization: Bearer <token>"
```

Response: `204 No Content`

## Social features

### Likes

* Like a post: POST `/careers/{id}/like/`
  
  Example:

  ```bash
  curl -X POST "http://localhost:8000/careers/1/like/" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `201 Created` with `{ "message": "Post liked successfully" }`

* Unlike a post: DELETE `/careers/{id}/unlike/`
  
  Example:

  ```bash
  curl -X DELETE "http://localhost:8000/careers/1/unlike/" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `204 No Content`

* List likes: GET `/careers/{id}/likes/?batch_size=10&batch_number=0`
  
  Example:

  ```bash
  curl -X GET "http://localhost:8000/careers/1/likes/?batch_size=10&batch_number=0" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `200 OK` with `likes` and `batch_info`

### Comments

* Add comment: POST `/careers/{id}/comment/`
  
  Body:

  ```json
  { "content": "This is a comment" }
  ```

  Example:

  ```bash
  curl -X POST "http://localhost:8000/careers/1/comment/" \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"content":"This is a comment"}'
  ```

  Response: `201 Created` with the comment

* List comments: GET `/careers/{id}/comments/?batch_size=10&batch_number=0`
  
  Example:

  ```bash
  curl -X GET "http://localhost:8000/careers/1/comments/?batch_size=10&batch_number=0" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `200 OK` with `comments` and `batch_info`

### Shares

* Share a post: POST `/careers/{id}/share/`
  Example:

  ```bash
  curl -X POST "http://localhost:8000/careers/1/share/" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `201 Created` with `{ "message": "Post shared successfully" }`

* List shares: GET `/careers/{id}/shares/?batch_size=10&batch_number=0`
  
  Example:

  ```bash
  curl -X GET "http://localhost:8000/careers/1/shares/?batch_size=10&batch_number=0" \
    -H "Authorization: Bearer <token>"
  ```

  Response: `200 OK` with `shares` and `batch_info`

* Create a shared post with new content: POST `/careers/{id}/share-post/`
  Body:

  ```json
  { "title": "Shared Post Title", "content": "My thoughts" }
  ```

  Example:

  ```bash
  curl -X POST "http://localhost:8000/careers/1/share-post/" \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"title":"Shared Post Title","content":"My thoughts"}'
  ```

  Response: `201 Created` with the new post (`post_type` is `"share"` and `original_post` present)



