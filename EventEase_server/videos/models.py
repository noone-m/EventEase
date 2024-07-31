from django.db import models
from services.models import Service

class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(Service,on_delete = models.CASCADE,null = True)