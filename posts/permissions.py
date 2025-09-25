from rest_framework import permissions


class IsPostAuthor(permissions.BasePermission):
    # custom permission to only allow authors to edit their own posts via x-username header
    
    def has_object_permission(self, request, view, obj):
        # read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # write permissions require x-username header
        username_header = request.META.get('HTTP_X_USERNAME')
        if not username_header:
            return False
        
        # check if the username matches the post author
        return obj.username == username_header

