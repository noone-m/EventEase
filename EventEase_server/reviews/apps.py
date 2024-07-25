from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    def ready(self):
        from .models import Review
        from .signals import update_product_avg_rating
        post_save.connect(update_product_avg_rating, sender=Review)  
        post_delete.connect(update_product_avg_rating, sender=Review)