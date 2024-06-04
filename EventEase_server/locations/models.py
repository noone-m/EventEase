from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=100,null = True)
    state = models.CharField(max_length=100,null = True)
    village_city = models.CharField(max_length=100,null = True) # city, town or village
    street = models.CharField(max_length=255,null = True)


class Location(models.Model):
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null =False)
    longitude = models.DecimalField(max_digits=12, decimal_places=9,null = False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null = False,related_name = 'location')
    class Meta:
        unique_together = ('latitude', 'longitude', 'address')