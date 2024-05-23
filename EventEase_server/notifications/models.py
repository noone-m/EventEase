from django.db import models
from accounts.models import User


class Message(models.Model):
    message = models.TextField()

class Notification(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    dest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
