# SocialHubAPI

A complete social API with CRUD operations for posts and social interactions including likes, comments, and shares.

## 📚 **Documentation**

- **[Posts API](POSTS_API.md)** - Complete CRUD operations for posts and social interactions
- **[Users API](USERS_API.md)** - User management, authentication, and profile features
- **[User Search API](USER_SEARCH_API.md)** - Advanced user search and filtering capabilities
- **[Social Features](SOCIAL_FEATURES.md)** - Likes, comments, shares, and user relationships
- **[Authentication](AUTHENTICATION.md)** - Authentication system and security features
- **[Frontend Integration Guide](FRONTEND_INTEGRATION.md)** - Best practices for frontend developers

## 🔧 **Quick Setup**

### Authentication
The API uses JWT authentication by default. No additional configuration needed.

### Installation
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

## 📋 **Base URLs**

- **Posts API**: `http://localhost:8000/careers/`
- **Users API**: `http://localhost:8000/users/`
- **API Documentation**: `http://localhost:8000/api/docs/`

## 🔐 **Authentication**

The API uses JWT (JSON Web Token) authentication for all authenticated requests:

```bash
# All authenticated requests
-H "Authorization: Bearer <jwt_token>"
```

## 🚀 **Quick Start Examples**

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
curl -X POST "http://localhost:8000/careers/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World!"}'
```

## 🧪 **Testing**

```bash
# Run all tests
python manage.py test

# Run specific test suites
python manage.py test posts
python manage.py test users
```

## 📁 **Project Structure**

```
socialhubapi/
├── posts/              # Posts API and social interactions
├── users/              # Users API and authentication
├── socialhubapi/       # Django settings and configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔗 **API Features Overview**

### Posts API
- Complete CRUD operations for posts
- Social interactions (likes, comments, shares)
- Pagination and filtering
- CodeLeap careers API compatibility

### Users API
- User registration and authentication
- Profile management
- JWT token-based security
- Social features (following/followers)

### User Search
- Advanced search and filtering
- Autocomplete suggestions
- Search statistics
- Multiple filter options

### Social Features
- Like/unlike posts
- Comment system
- Share functionality
- User relationships
- Personalized feeds

## 📊 **Status Codes**

- **200 OK** - Successful operation
- **201 Created** - Resource created
- **204 No Content** - Successful operation with no content
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **409 Conflict** - Resource already exists

---

For detailed information about each feature, please refer to the specific documentation files linked above.

