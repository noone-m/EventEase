from django.db import models
from accounts.models import User
from services.models import Service


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)

