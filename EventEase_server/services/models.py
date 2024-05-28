from django.conf import settings
from django.db import models
from locations.models import Location


class ServiceType(models.Model):
    type = models.CharField(max_length=255)


class ServiceProviderApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null = False)
    service_type = models.ForeignKey(ServiceType,on_delete = models.SET_NULL, null = True)
    otherType = models.CharField(max_length = 50, null=True)
    phone = models.CharField(max_length = 15,null = False)
    national_identity_front = models.ImageField(upload_to='identity/')
    national_identity_back = models.ImageField(upload_to='identity/')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f'{self.user.email} - {self.service_type}'

class Service(models.Model):
    service_provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.ForeignKey(ServiceType,on_delete = models.CASCADE)
    phone = models.CharField(max_length = 15,null = False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now= True, null = True)

    def __str__(self):
        return self.name
    

class FoodService(Service):
    cuisine_type = models.CharField(max_length=255)
    menu = models.TextField()

 
class FoodType(models.Model):
    type = models.CharField(max_length=255)

# class foodtypeservice breaks manytomany relationship between foodservice foodtype 
class FoodTypeService(models.Model):
    foodService = models.ForeignKey(FoodService,on_delete = models.CASCADE)
    foodType = models.ForeignKey(FoodType,on_delete = models.CASCADE) 

class DJService(Service):
    music_genre = models.CharField(max_length=255)
    equipment_provided = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    area_limit_km = models.IntegerField()

class FavoriteService(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service =  models.ForeignKey(Service, on_delete=models.CASCADE)