from django.conf import settings
from django.db import models
from locations.models import Location


class ServiceType(models.Model):
    type = models.CharField(max_length=255)


class ServiceProviderApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null = False,related_name = 'serviceProviderApplication')
    service_type = models.ForeignKey(ServiceType,on_delete = models.SET_NULL, null = True,related_name = 'serviceType')
    otherType = models.CharField(max_length = 50, null=True)
    phone = models.CharField(max_length = 15,null = False)
    national_identity_front = models.ImageField(upload_to=r'storage/pictures/identity/',null = False)
    national_identity_back = models.ImageField(upload_to=r'storage/pictures/identity/',null = False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],default = 'Pending')
    created_at = models.DateTimeField(auto_now_add = True, null = True)
#updated at
    def __str__(self):
        return f'{self.user.email} - {self.service_type}'

class Service(models.Model):
    service_provider = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null = True)
    service_type = models.ForeignKey(ServiceType,on_delete = models.CASCADE)
    # in future phone should be unique
    phone = models.CharField(max_length = 15,null = False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now= True, null = True)
    
    def __str__(self):
        return self.name


class FoodType(models.Model):
    type = models.CharField(max_length=255)


class FoodService(Service):
    area_limit_km = models.IntegerField(null = True)


class Food(models.Model):
    food_type = models.ForeignKey(FoodType,on_delete =models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    ingredients = models.TextField(null = True)


class FoodServiceFood(models.Model):
    foodService = models.ForeignKey(FoodService,on_delete = models.CASCADE)
    food = models.ForeignKey(Food,on_delete = models.CASCADE) 


# class foodtypeservice breaks manytomany relationship between foodservice foodtype 
class FoodTypeService(models.Model):
    foodService = models.ForeignKey(FoodService,on_delete = models.CASCADE)
    foodType = models.ForeignKey(FoodType,on_delete = models.CASCADE) 


class DJService(Service):
    music_genre = models.CharField(max_length=255)
    equipment_provided = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    area_limit_km = models.IntegerField()

#   what if venue provide food?
class Venue(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    capacity = models.IntegerField()
    amenities = models.TextField() # like wifi,parking,audio-visual devices
    minimum_guests = models.IntegerField()
    maximum_guests = models.IntegerField()
    

class PhotoGrapherService(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    area_limit_km = models.IntegerField()


class DecorationService(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    area_limit_km = models.IntegerField()

class EntertainementService(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    area_limit_km = models.IntegerField()


class Decore(models.Model):
    decore_service = models.ForeignKey(DecorationService,on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    quantity  = models.IntegerField()
    avialable_quantity  = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    photo = models.ImageField(upload_to=r'storage/pictures/decores/',null = False)

class DecoreType(models.Model):
    event_type = models.ForeignKey('events.EventType',on_delete=models.CASCADE)
    decore = models.ForeignKey(Decore,on_delete=models.CASCADE)

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.service.name} on {self.date}"

class FavoriteService(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service =  models.ForeignKey(Service, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'service')