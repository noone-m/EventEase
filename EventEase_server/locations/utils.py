import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Address, Location

def get_location_from_osm(latitude,longitude):
    # without this header your going to get 403 Forbidden
    user_agent = "my-application localhost" 
    accept_language = "en-US"
    headers = {'User-Agent': user_agent,'Accept-Language' : accept_language} 
    response = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1',headers=headers)

    if response.status_code == 200:
        osm_data = response.json()
        try:
            osm_address = osm_data['address']
        except KeyError:
            raise ValidationError({'message':'try another location please'})
        # openStreetMap API can return city,town,village...etc
        places = ['city','town','village']
        village_city = None
        state = None
        country = None
        for place in places:
            if place in osm_address.keys():
                village_city = osm_address[place]
        try :       
            state = osm_address['state']
            country = osm_address['country']
        except Exception:
            pass
        if village_city is None or state is None or country is None:
            raise ValidationError({'message':'try another location please'})
        
        address,created = Address.objects.get_or_create(
            country = country,
            state = state,
            village_city = village_city
        )
        # if there is street name add it
        try:
            street = osm_address['road']
            address.street= street
            address.save()
        except KeyError:
            pass
        location,created = Location.objects.get_or_create(
            latitude = latitude,
            longitude = longitude,
            address = address
        )
        return location
    else:
        print('messi')
        raise ValidationError(response.text,status = response.status_code)