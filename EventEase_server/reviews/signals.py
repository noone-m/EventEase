from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_avg_rating(sender, instance, **kwargs): # we may use async here
    instance.service.update_average_rating()