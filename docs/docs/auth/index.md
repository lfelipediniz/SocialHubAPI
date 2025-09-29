# Authentication System Documentation

## Overview
The SocialHub API uses JWT (JSON Web Token) authentication for secure access to all endpoints.

## Authentication System

### JWT Authentication
- **Purpose**: Secure token-based authentication
- **Method**: JWT (JSON Web Token) authentication
- **Header**: `Authorization: Bearer <access_token>`
- **Token Lifetime**: Access tokens expire after 60 minutes
- **Refresh Tokens**: Available for 7 days

## Configuration

### Environment Variables
Configure JWT settings using environment variables:

```bash
# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Settings Configuration
JWT configuration is set in `settings.py`:

```python
# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_SECRET_KEY', default=SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

## Authentication Workflow

### 1. User Registration
```bash
curl -X POST "http://localhost:8000/users/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepassword123",
    "first_name": "Alice",
    "last_name": "Smith"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. User Login
```bash
curl -X POST "http://localhost:8000/users/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Using Access Tokens
Include the access token in the Authorization header for protected endpoints:

```bash
curl -X GET "http://localhost:8000/users/me/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Token Refresh
When the access token expires, use the refresh token to get a new one:

```bash
curl -X POST "http://localhost:8000/users/token/refresh/" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 5. User Logout
To logout, blacklist the refresh token:

```bash
curl -X POST "http://localhost:8000/users/logout/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Response:**
```json
{
  "message": "successfully logged out"
}
```

## Protected Endpoints

All endpoints except the following require authentication:
- `POST /users/register/` - User registration
- `POST /users/login/` - User login
- `POST /users/token/refresh/` - Token refresh

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "message": "Access denied - You can only edit your own posts"
}
```

### Invalid Token
```json
{
  "detail": "Given token not valid for any token type"
}
```

## Security Features

- **Token Rotation**: Refresh tokens are rotated on each use
- **Token Blacklisting**: Logged out tokens are blacklisted
- **Secure Headers**: Tokens must be sent in Authorization header
- **HTTPS Recommended**: Use HTTPS in production for secure token transmission