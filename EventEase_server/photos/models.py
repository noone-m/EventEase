from django.db import models
from services.models import Service,Food

class ServicePhotos(models.Model):
    image  = models.ImageField(upload_to='storage/pictures/services/')
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image)
        return None

class FoodPhotos(models.Model):
    image  = models.ImageField(upload_to='storage/pictures/foods/')
    food = models.ForeignKey(Food, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)