from django.conf import settings
from django.db import models
from accounts.models import User
from locations.models import Location

class EventType(models.Model):
    name = models.CharField(max_length=255)

# if there is event type there should be no othertype and in reverse
class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default= 0.0)


class InvitationCard(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    invitation = models.TextField()
    