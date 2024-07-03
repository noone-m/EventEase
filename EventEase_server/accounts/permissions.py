from rest_framework.permissions import BasePermission,SAFE_METHODS,IsAuthenticated
from  .models import OTP,EmailVerified


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.user
        except AttributeError:
            return request.user == obj.service_provider
    

class IsOwnerOrAdminUser(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to view it.
    """
    def has_permission(self, request, view):
        return IsAuthenticated()
    
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner or an admin
        print('object level')
        return obj.user == request.user or request.user.is_superuser
class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsPhoneVerified(BasePermission):
    """
    Allows access  to users who verified thier numbers.
    """

    def has_permission(self, request, view):
        try:
            otp = OTP.objects.get(user = request.user)
        except OTP.DoesNotExist:
            return False
        
        return otp.is_verified


class IsEmailVerified(BasePermission):
    """
    Allows access  to users who verified thier numbers.
    """

    def has_permission(self, request, view):
        try:
            emailVerified = EmailVerified.objects.get(user = request.user)
        except EmailVerified.DoesNotExist:
            return False
        return EmailVerified.is_verified      