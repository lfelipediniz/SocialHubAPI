# SocialHubAPI Documentation

Welcome to the SocialHubAPI documentation. This project provides a complete social API with CRUD operations for posts and social interactions including likes, comments, and shares.

## Quick Start

Get up and running with SocialHubAPI:

```bash
# activate virtual environment
source venv/bin/activate
```

```bash
# install dependencies
pip install -r requirements.txt
```

```bash
# run migrations
python manage.py migrate
```

```bash
# start server
python manage.py runserver 0.0.0.0:8000
```

## Documentation Overview

### API Reference

* [Posts API](api/posts.md) — CRUD operations for posts and interactions
* [Users API](api/users.md) — User management, authentication, profiles
* [Social Features](api/social.md) — Likes, comments, shares, relationships
* [Routes Overview](api/routes.md) — Complete endpoint list

### Authentication

* [Authentication System](auth/index.md) — Guide for JWT token usage

### Guides

* [Quick Start Guide](quickstart.md) — Simple setup with examples
* [Development Guide](development.md) — Local setup and best practices

## Configuration

### JWT Authentication

The API uses JWT tokens for secure authentication. Configure your secret key:

```bash
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## Base URLs

* Posts API: `http://localhost:8000/careers/`
* Users API: `http://localhost:8000/users/`
* API Docs: `http://localhost:8000/api/docs/`

## Authentication

Use JWT tokens in all requests:

```bash
-H "Authorization: Bearer <jwt_token>"
```

## Examples

### Register and Use the API

```bash
# 1. Register user
curl -X POST "http://localhost:8000/users/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "password123", "password_confirm": "password123"}'
```

```bash
# 2. Login and save token
TOKEN=$(curl -X POST "http://localhost:8000/users/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}' | jq -r '.access')
```

```bash
# 3. Use token for API calls
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World!"}'
```

