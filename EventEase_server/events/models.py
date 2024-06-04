from django.db import models
from services.models import Service
from accounts.models import User
from locations.models import Location

class EventType(models.Model):
    name = models.CharField(max_length=255)

# if there is event type there should be no othertype and in reverse
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    other_type = models.CharField(max_length = 255,null =True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE) # i think i should put this to model.SET_Default using some default value like Delete in Event table
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)


