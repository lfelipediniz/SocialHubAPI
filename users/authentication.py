from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameAuthentication(authentication.BaseAuthentication):
    """
    custom authentication that only requires username
    used when AUTHENTICATION_REQUIRED=False
    """
    
    def authenticate(self, request):
        # get username from header or query parameter
        username = None
        
        # try to get from X-Username header (for posts api compatibility)
        username = request.META.get('HTTP_X_USERNAME')
        
        # try to get from Authorization header (username only)
        if not username:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Username '):
                username = auth_header.replace('Username ', '')
        
        # try to get from query parameter
        if not username:
            username = request.GET.get('username')
        
        if not username:
            return None
        
        try:
            # get or create user with just username
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',  # dummy email
                    'is_active': True,
                }
            )
            return (user, None)  # no credentials needed
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('invalid username')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'authentication error: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Username'
