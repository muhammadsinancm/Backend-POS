from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "Only the owner can perform this action."
    
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated 
                and (request.user.is_superuser or 
                     request.user.role == 'owner')
                )
        
class IsCashier(BasePermission):
    message = "Only cashiers can perform this action."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'cashier')
    
class IsKitchen(BasePermission):
    message = "Only kitchen staff can perform this action."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'kitchen')
    
class IsWaiter(BasePermission):
    message = "Only waiters can perform this action."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'waiter')
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Owners can modify menu data.
    Authenticated users can read it.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        return (request.user.is_superuser or request.user.role == 'owner')