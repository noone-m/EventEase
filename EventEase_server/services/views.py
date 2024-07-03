from django.shortcuts import get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUser,IsOwner,IsOwnerOrAdminUser
# from locations.serializers import LocationSerializer
from locations.models import Address, Location
from locations.serializers import AddressSerializer,LocationSerializer
from .models import ServiceType,Service,FoodService,ServiceProviderApplication,FavoriteService
from .serializers import FoodServiceSerializer,ServiceTypeSerializer,ServiceProviderApplicationSerializer,FavoriteServiceSerializer,ServiceSerializer,DJServiceSerializer


class ServiceTypeViewSet(ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAdminUser]


class FoodServiceViewSet(ModelViewSet):
    queryset = FoodService.objects.all()
    serializer_class = FoodServiceSerializer
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser|IsOwner]
        elif self.action in['list','create']:
            self.permission_classes = [IsAdminUser]
        else:
            pass
        return super().get_permissions()

#there should be thruttle on how many times he can submit the application
class ServiceProviderApplicationView(APIView):

    def post(self, request):
        location_serializer = LocationSerializer(data=request.data)
        applicatoin_serializer = ServiceProviderApplicationSerializer(data=request.data)
        user = request.user
        applications = ServiceProviderApplication.objects.filter(user = request.user)
        for application in applications:
            if application.status in ['Approved','Pending']:
                return Response({'message': 'if you have approved application or pending one you can not send another application'}, status=status.HTTP_400_BAD_REQUEST)
        if location_serializer.is_valid():

            latitude = location_serializer.validated_data['latitude']
            longitude = location_serializer.validated_data['longitude']
            # without this header your going to get 403 Forbidden
            user_agent = "my-application localhost" 
            accept_language = "en-US"
            headers = {'User-Agent': user_agent,'Accept-Language' : accept_language} 
            response = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1',headers=headers)

            if response.status_code == 200:
                osm_data = response.json()
                osm_address = osm_data['address']
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
                    return Response({'message': 'Try another location please'}, status=status.HTTP_400_BAD_REQUEST)
                
                address,created = Address.objects.get_or_create(
                    country = country,
                    state = state,
                    village_city = village_city
                )
                # if there is street name add it
                street = osm_address['road']
                if street is not None :
                    address.street= street
                    address.save()
                
                location,created = Location.objects.get_or_create(
                    latitude = latitude,
                    longitude = longitude,
                    address = address
                )
                print('created?')
                print(created)
                if applicatoin_serializer.is_valid():
                    applicatoin_serializer.save(location = location,user = user)
                    return Response({'message': 'Service Provider Application created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(applicatoin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Could not fetch data from OpenStreetMap'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        if request.user.is_superuser:
            applications = ServiceProviderApplication.objects.all()
        else : 
            applications = ServiceProviderApplication.objects.filter(user = request.user)
        application_serializer = ServiceProviderApplicationSerializer(applications,many = True,context = {'request':request})
        return Response(application_serializer.data)
    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT']:
            return [IsOwner()] 


class ServiceProviderApplicationDetailView(APIView):


    def get(self, request, pk):
        try:
            application = ServiceProviderApplication.objects.get(id=pk)
            self.check_object_permissions(self.request, application)
        except ServiceProviderApplication.DoesNotExist:
            return Response({'message':'application does not exist'},status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceProviderApplicationSerializer(application, context={'request': request})
        return Response(serializer.data)


    def put(self, request, pk):
        try:
            application = ServiceProviderApplication.objects.get(id=pk)
            self.check_object_permissions(self.request, application)
        except ServiceProviderApplication.DoesNotExist:
            return Response({'message':'application does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        if application.status == 'Pending' :
            pass
        else : 
            return Response({'message':'you can update application only when status is pending '},status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceProviderApplicationSerializer(application, data=request.data, partial = True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsOwnerOrAdminUser()]
        elif self.request.method == 'PUT':
            return [IsOwner()] 

class ApproveApplication(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request,**kwargs):
        pk = kwargs.get('pk')
        application = ServiceProviderApplication.objects.get(id=pk)
        application.status = 'Approved'
        user = application.user
        user.is_service_provider = True
        application.save()
        user.save()
        if application.service_type.type == 'food': 
            service,created = FoodService.objects.get_or_create(
                service_provider = user,
                name = application.name,
                service_type = application.service_type,
                phone = application.phone,
                location = application.location
            )
            service.save()
            
        # if application.service_type.type == 'venue': 
        #     service,created = FoodService.objects.get_or_create(
        #         service_provider = user,
        #         name = application.name,
        #         service_type = application.service_type,
        #         phone = application.phone,
        #         location = application.location
        #     )
        #     service.save()
            return Response({'message':'approved'},status= status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
#Implement this in a function
class DeclineApplication(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request,**kwargs):
        pk = kwargs.get('pk')
        application = ServiceProviderApplication.objects.get(id=pk)
        application.status = 'Rejected'
        application.save()
        return Response({'m':'service has been declined successfully'})


class UserFavoriteServices(APIView):
    def get(self,requset,**kwargs):
        user = requset.user
        favorite_services = FavoriteService.objects.filter(user = user)
        print(favorite_services)
        serialzer = FavoriteServiceSerializer(favorite_services,many = True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
    def post(self,requset,**kwargs):
        user = requset.user
        serialzer = FavoriteServiceSerializer(data = requset.data)
        if serialzer.is_valid():
            serialzer.save(user = user)
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors)

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()

    def get_serializer_class(self):

        if self.action in ['list','create']:
            serializer =  ServiceSerializer
        elif self.action in ['retrieve','update','partial_update']:
            pk = self.kwargs.get('pk')
            try:
                service = Service.objects.get(id=pk)
                if service.service_type.type == 'food':
                    return FoodServiceSerializer
                elif service.service_type.type == 'DJ':
                    return DJServiceSerializer
            except Service.DoesNotExist:
                raise ValidationError(f"No service found with primary key {pk}")
        return serializer

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print(f"Updating instance: {instance.id}, current area_limit_km: {instance.area_limit_km}")
        
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         print(f"Updated instance: {serializer.data}")
    #     else:
    #         print(f"Validation errors: {serializer.errors}")
        
    #     return Response(serializer.data)

    # def perform_update(self, serializer):
    #     serializer.save()

    def get_object(self):
        # Override get_object to return the correct subclass instance
        obj = super().get_object()
        return self.get_subclass_instance(obj.id)

    def get_subclass_instance(self, pk):
        service = get_object_or_404(Service, pk=pk)
        if service.service_type.type == 'food':
            return FoodService.objects.get(pk=pk)
        elif service.service_type.type == 'DJ':
            pass
        return service
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser|IsOwner]
        elif self.action in['create']:
            self.permission_classes = [IsAdminUser]
        elif self.action in['list','retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            pass
        return super().get_permissions()

