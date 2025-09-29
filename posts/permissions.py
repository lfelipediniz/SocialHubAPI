from rest_framework import permissions


class IsPostAuthor(permissions.BasePermission):
    # custom permission to only allow authors to edit their own posts
    # uses JWT authentication
    
    def has_object_permission(self, request, view, obj):
        # read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # write permissions require JWT authentication
        if not request.user.is_authenticated:
            return False
        
        # check if the authenticated user is the post author
        return obj.user == request.user

