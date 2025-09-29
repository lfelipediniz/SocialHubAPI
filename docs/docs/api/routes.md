# API Routes Reference


## Authentication Header

Authorization: Bearer <jwt_token>


## Standard Response Format

```json
{
  "message": "Success message",
  "data": [...],
  "batch_info": {
    "current_batch": 0,
    "batch_size": 10,
    "total_items": 25,
    "total_batches": 3,
    "items_in_current_batch": 10
  }
}
```

## Pagination and Filtering

### Pagination (Batch System)

* `batch_size` – Number of items per page

* `batch_number` – Starts at 0

### Search & Filtering

* `search` – General search term

* `q` – Alias for search

* `first_name` – Filter by first name

* `last_name` – Filter by last name

* `ordering` – Sort results

* `limit` – Limit number of results

## Posts API

### Posts Management

* `GET /careers/` – List all posts

* `POST /careers/create/` – Create new post

* `GET /careers/{id}/` – Get specific post

* `PATCH /careers/{id}/` – Update post

* `DELETE /careers/{id}/` – Delete post

### Social Interactions

* `POST /careers/{id}/like/` – Like a post

* `DELETE /careers/{id}/unlike/` – Unlike a post

* `GET /careers/{id}/likes/` – List likes

* `POST /careers/{id}/comment/` – Add comment

* `GET /careers/{id}/comments/` – List comments

* `POST /careers/{id}/share/` – Share a post

* `GET /careers/{id}/shares/` – List shares

## Users API

### Authentication

* `POST /careers/users/register/` – Register new user

* `POST /careers/users/login/` – Login

* `POST /careers/users/logout/` – Logout

* `POST /careers/users/token/refresh/` – Refresh token

### User Management

* `GET /careers/users/` – List all users

* `GET /careers/users/me/` – Get current user profile

* `PATCH /careers/users/me/update/` – Update current user

* `GET /careers/users/me/stats/` – Get user statistics

* `GET /careers/users/{username}/` – Get profile by username

### Social Features

* `POST /careers/users/follow/` – Follow a user

* `GET /careers/users/following/` – List following users

* `GET /careers/users/followers/` – List my followers

* `GET /careers/users/{username}/followers/` – List user's followers

* `GET /careers/users/{username}/following/` – List who user follows

* `DELETE /careers/users/{username}/unfollow/` – Unfollow user

## Errors

### Status codes

* 200 OK

* 201 Created

* 204 No Content

* 400 Bad Request

* 401 Unauthorized

* 403 Forbidden

* 404 Not Found

* 409 Conflict

### Error format

```json
{ "error": "Error message", "details": "Additional error details" }
```
