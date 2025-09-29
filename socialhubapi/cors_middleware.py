from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class CustomCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add CORS headers for all requests
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Methods'] = 'DELETE, GET, OPTIONS, PATCH, POST, PUT'
        response['Access-Control-Allow-Headers'] = 'accept, authorization, content-type, user-agent, x-csrftoken, x-requested-with, x-username'
        response['Access-Control-Max-Age'] = '86400'
        
        return response
