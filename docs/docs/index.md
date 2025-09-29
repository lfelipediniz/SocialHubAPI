# SocialHubAPI Documentation

Welcome to the SocialHubAPI documentation! This is a complete social API with CRUD operations for posts and social interactions including likes, comments, and shares.

## 🚀 Quick Start

Get up and running with SocialHubAPI in minutes:

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

## 📚 Documentation Overview

### API Reference
- **[Posts API](api/posts.md)** - Complete CRUD operations for posts and social interactions
- **[Users API](api/users.md)** - User management, authentication, and profile features
- **[Social Features](api/social.md)** - Likes, comments, shares, and user relationships

### Authentication
- **[Authentication System](auth/index.md)** - Complete authentication guide with JWT tokens

### Guides
- **[Quick Start Guide](quickstart.md)** - Get started quickly with examples
- **[Development Guide](development.md)** - Development setup and best practices

## 🔧 Configuration

### JWT Authentication
The API uses JWT tokens for secure authentication. Configure your JWT secret:
```bash
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## 📋 Base URLs

- **Posts API**: `http://localhost:8000/careers/`
- **Users API**: `http://localhost:8000/users/`
- **API Documentation**: `http://localhost:8000/api/docs/`

## 🔐 Authentication

### JWT Authentication
```bash
# All APIs
-H "Authorization: Bearer <jwt_token>"
```

## 🚀 Quick Examples

### Complete Platform Usage
```bash
# 1. Register user
curl -X POST "http://localhost:8000/users/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "password123", "password_confirm": "password123"}'

# 2. Login and save token
TOKEN=$(curl -X POST "http://localhost:8000/users/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}' | jq -r '.access')

# 3. Use token for API calls
curl -X POST "http://localhost:8000/careers/create/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World!"}'
```
