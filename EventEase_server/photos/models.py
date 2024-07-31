from django.db import models
from services.models import Service,Food,Decor

class ServicePhotos(models.Model):
    image  = models.ImageField(upload_to='pictures/services/')
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image)
        return None

class FoodPhotos(models.Model):
    image  = models.ImageField(upload_to='pictures/foods/')
    food = models.ForeignKey(Food, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)


class ServiceProfilePhoto(models.Model):
    service = models.OneToOneField(Service,on_delete= models.CASCADE)
    servicePhoto = models.ImageField(upload_to='pictures/services/profile_photos')
    

class MainFoodPhoto(models.Model):
    food = models.OneToOneField(Food, on_delete = models.CASCADE)
    foodPhoto = models.ForeignKey(FoodPhotos,on_delete=models.CASCADE)
    
        
class DecorPhotos(models.Model):
    image  = models.ImageField(upload_to='pictures/decors/')
    decor = models.ForeignKey(Decor, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)

class MainDecorPhoto(models.Model):
    decor = models.OneToOneField(Decor, on_delete = models.CASCADE)
    decorPhoto = models.ForeignKey(DecorPhotos,on_delete=models.CASCADE)