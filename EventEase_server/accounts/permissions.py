from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission,SAFE_METHODS,IsAuthenticated
from services.models import Service
from  .models import OTP,EmailVerified



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.user
        except AttributeError:
            return request.user == obj.service_provider

class IsServiceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print('has_object_permission')
        try:
            return request.user == obj.service.service_provider
        except AttributeError:
            return False
        
    def has_permission(self, request, view):
        try : 
            service_pk = view.kwargs['service_pk']
        except KeyError:
            service_pk = view.kwargs['pk']
        service = get_object_or_404(Service,id = service_pk)
        return service.service_provider == request.user
    

class IsOwnerOrAdminUser(BasePermission):
    """
    Custom permission to grant only owners of an object or admin users the permissoins.
    """
    def has_permission(self, request, view):
        return IsAuthenticated()
    
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner or an admin
        print('object level')
        try:
            return obj.reporter == request.user or request.user.is_superuser
        except AttributeError:
            pass
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
        return emailVerified.is_verified      
    

class IsServiceOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        is_service_owner = IsServiceOwner()
        is_admin_user = IsAdminUser()
        return is_service_owner.has_permission(request,view) or is_admin_user.has_permission(request,view)
    
class DefaultOrIsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or IsEmailVerified().has_permission(request, view) and IsPhoneVerified().has_permission(request, view)