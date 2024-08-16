from django.conf import settings
from django.db import models
from django.db.models import Avg
from locations.models import Location
from events.models import Event
from rest_framework.response import  Response

class ServiceType(models.Model):
    type = models.CharField(max_length=255, unique=True)


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
    avg_rating = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now= True, null = True)
    
    def __str__(self):
        return self.name

    def update_average_rating(self):
        avg_rating = self.service_reviews.aggregate(Avg('rating'))['rating__avg']
        self.avg_rating = avg_rating
        self.num_ratings = self.service_reviews.count()
        self.save()

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
    music_genre = models.CharField(max_length=255, null = True)
    equipment_provided = models.TextField(null = True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null = True) 
    area_limit_km = models.IntegerField(null = True)

class Venue(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null = True) 
    capacity = models.IntegerField(null = True)
    amenities = models.TextField(null = True) # like wifi,parking,audio-visual devices
    

class PhotoGrapherService(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null = True) 
    area_limit_km = models.IntegerField(null = True)


class DecorationService(Service):
    area_limit_km = models.IntegerField(null = True)

class EntertainementService(Service):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null = True) 
    area_limit_km = models.IntegerField(null = True)


class Decor(models.Model):
    decor_service = models.ForeignKey(DecorationService,on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    quantity  = models.IntegerField()
    available_quantity  = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,null = True)
    price =  models.DecimalField(max_digits=10, decimal_places=2, null = True)
    description = models.TextField(null=True)

    def clean(self):
        super().clean()
        if self.hourly_rate is None and self.price is None:
            return Response({'message':'Either hourly_rate or price must be provided.'},status=400)
        
    def save(self, *args, **kwargs):
        self.available_quantity = self.quantity
        self.clean()
        super().save(*args, **kwargs)


class DecorEventType(models.Model):
    event_type = models.ForeignKey('events.EventType',on_delete=models.CASCADE)
    decor = models.ForeignKey(Decor,on_delete=models.CASCADE)
    

class FavoriteService(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service =  models.ForeignKey(Service, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'service')


class Reservation(models.Model):
    """
    Base model for different types of reservations (e.g., services, decorations).
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Rejected','Rejected'), ('Paid','Paid')], 
        default='Pending'
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now= True, null = True)



class ServiceReservation(Reservation):
    """
    Model for reserving general services.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"ServiceReservation for {self.service} on {self.start_time} to {self.end_time}"


class DecorsReservation(Reservation):
    """
    Model for reserving decors
    """
    decor_service = models.ForeignKey(DecorationService, on_delete=models.CASCADE)

    def __str__(self):
        return f"DecorReservation for {self.decor_service} on {self.start_time} to {self.end_time}"


class DecorsInReservation(models.Model):
    decors_reservation = models.ForeignKey(DecorsReservation, on_delete=models.CASCADE)
    decor = models.ForeignKey(Decor,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.FloatField()


class Order(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete= models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'),('Rejected','Rejected'), ('Paid','Paid')])
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date= models.DateTimeField()


class FoodInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()




