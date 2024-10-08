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
    
    def get_all_paid_reservations(self):
        from services.models import Reservation
        reservations = Reservation.objects.filter(event=self,status='Paid').all()
        return reservations
    
    def get_all__paid_orders(self):
        from services.models import Order
        orders = Order.objects.filter(event=self, status='Paid').all()
        return orders
    
    def compute_total_cost(self):
        total_cost = 0
        reservations = self.get_all_paid_reservations()
        orders = self.get_all__paid_orders()
        for reservation in reservations:
            total_cost = total_cost + float(reservation.cost)
        for order in orders:
            total_cost = total_cost + float(order.total_price)
        self.total_cost = total_cost
        self.save()
        return self.total_cost

class InvitationCardDesign(models.Model):
    image = models.ImageField(upload_to='pictures/card_design')
    image_width = models.IntegerField()
    image_hieght = models.IntegerField()
    width= models.IntegerField()
    hight= models.IntegerField()
    start_x = models.IntegerField()
    start_y = models.IntegerField()

    
class InvitationCard(models.Model):
    design = models.ForeignKey(InvitationCardDesign,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    title = models.CharField(max_length=100)


