from rest_framework.permissions import BasePermission,SAFE_METHODS
from  .models import OTP
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    
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