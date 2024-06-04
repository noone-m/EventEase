from django.db import models
from services.models import Service,Food

class ServicePhotos(models.Model):
    url  = models.ImageField(upload_to='storage/pictures/services/')
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)


class FoodPhotos(models.Model):
    url  = models.ImageField(upload_to='storage/pictures/foods/')
    food = models.ForeignKey(Food, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)