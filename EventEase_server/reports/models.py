from django.db import models
from django.conf import settings

# I should implemet something like when the report get solved the user should recieve a notification about the result
class ReportReview(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name = 'review_reports')
    review = models.ForeignKey('reviews.Review', on_delete=models.CASCADE)
    reason = models.TextField()
    is_solved = models.BooleanField(default = False)
    solved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name = 'solved_review_reports')


class ReportService(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'service_reports')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    reason = models.TextField()
    evidence = models.FileField(upload_to='storage/reports/evidence/', null=True, blank=True)
    resolution = models.CharField(max_length=255, null=True, blank=True)#refund, apology, service correction
    is_solved = models.BooleanField(default = False)
    solved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'solved_service_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
