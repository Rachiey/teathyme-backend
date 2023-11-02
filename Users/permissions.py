from rest_framework import permissions

class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for editing a user
    """

    edit_methods = ("PUT", "PATCH")
    message = "You can't edit that user!"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True
        
        return obj == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to extend from to allow only admin access or read-only access
    """
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        # Needs to be authenticated for basic access
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_superuser:
            return True

        # Anyone can access GET, OPTIONS, HEAD methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Staff users have delete access
        if request.user.is_staff and request.method not in self.edit_methods:
            return True
        
        # Otherwise deny access
        return False


class IsPosterOrReadOnly(IsAdminOrReadOnly):
    """
    Custom permission extension to only allow owners of a post or admins to edit it
    """
    message = "You do not have permission to edit this post!"

    def has_permission(self, request, view):
        return super(IsPosterOrReadOnly, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        
        # Posters can edit/delete their posts
        if obj.poster == request.user:
            return True

        # Otherwise use the base IsAdminOrReadOnly permissions
        return super(IsPosterOrReadOnly, self).has_object_permission(request, view, obj)


class IsCommenterOrReadOnly(IsAdminOrReadOnly):
    """
    Custom permission extension to only allow owners of a comment or admins to edit it
    """
    message = "You do not have permission to edit this comment!"

    def has_permission(self, request, view):
        return super(IsCommenterOrReadOnly, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        
        # Commenters can edit/delete their posts
        if obj.commenter == request.user:
            return True

        # Otherwise use the base IsAdminOrReadOnly permissions
        return super(IsCommenterOrReadOnly, self).has_object_permission(request, view, obj)