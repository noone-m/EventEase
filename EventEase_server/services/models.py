from django.conf import settings
from django.db import models
from locations.models import Location


class ServiceType(models.Model):
    type = models.CharField(max_length=255)


class ServiceProviderApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    serviceType = models.ForeignKey(ServiceType,on_delete = models.SET_NULL, null = True)
    otherType = models.CharField(max_length = 50)
    national_identity_front = models.ImageField(upload_to='identity/')
    national_identity_back = models.ImageField(upload_to='identity/')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])


class Service(models.Model):
    service_provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.ForeignKey(ServiceType,on_delete = models.SET_NULL, null = True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    area_limit_km = models.IntegerField()

class FavoriteService(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service =  models.ForeignKey(Service, on_delete=models.CASCADE)