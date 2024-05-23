from django.db import models
from services.models import Service


class Photos(models.Model):
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    url  = models.ImageField(upload_to='services/')
