from django.urls import path,include
from .views import GetToken,log_out

urlpatterns = [
    # path('register', views.register),
    path('log-in', GetToken.as_view()),
    path('log-out', log_out),
]