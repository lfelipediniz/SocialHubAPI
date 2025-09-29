from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings


class CustomCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Get origin from request
        origin = request.META.get('HTTP_ORIGIN')
        
        # Check if origin is in allowed origins
        if origin in settings.CORS_ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        else:
            # Default to first allowed origin if origin not found
            response['Access-Control-Allow-Origin'] = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:8080'
        
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Methods'] = 'DELETE, GET, OPTIONS, PATCH, POST, PUT'
        response['Access-Control-Allow-Headers'] = 'accept, authorization, content-type, user-agent, x-csrftoken, x-requested-with, x-username'
        response['Access-Control-Max-Age'] = '86400'
        
        return response
