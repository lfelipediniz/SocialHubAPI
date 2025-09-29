# Quick Start Guide

Get up and running with SocialHubAPI in minutes.

## Prerequisites

- Python 3.12+
- PostgreSQL (recommended for production)
- Git

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/lfelipediniz/SocialHubAPI.git
cd SocialHubAPI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp env.example .env
```

Edit `.env` file:
```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:password@localhost:5432/socialhubapi

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here

# CORS Settings
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start Server
```bash
python manage.py runserver 0.0.0.0:8000
```

API available at `http://localhost:8000/`

## Quick Examples

### User Registration
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

### User Login
```bash
curl -X POST "http://localhost:8000/users/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepassword123"
  }'
```

### Create Post (with token)
```bash
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "Hello, SocialHubAPI!"
  }'
```

### List Posts
```bash
curl -X GET "http://localhost:8000/careers/"
```

### Like a Post
```bash
curl -X POST "http://localhost:8000/careers/1/like/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Add a Comment
```bash
curl -X POST "http://localhost:8000/careers/1/comment/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great post!"}'
```

## Next Steps

1. **Explore the API**: Check out the [API Reference](api/routes.md) for all available endpoints
2. **Authentication**: Learn about [JWT Authentication](auth/index.md) 

## API Documentation

- **[Routes Reference](api/routes.md)** - Quick reference of all endpoints
- **[Posts API](api/posts.md)** - Complete CRUD operations for posts
- **[Users API](api/users.md)** - User management and authentication
- **[Social Features](api/social.md)** - Likes, comments, shares, and relationships