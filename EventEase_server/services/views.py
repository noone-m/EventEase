import ast
from django.shortcuts import get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from accounts.permissions import IsAdminUser,IsOwner,IsOwnerOrAdminUser,IsServiceOwnerOrAdmin,Default,DefaultOrIsAdminUser
# from locations.serializers import LocationSerializer
from locations.models import Address, Location
from locations.serializers import AddressSerializer,LocationSerializer

from events.models import EventType, Event

from .models import (ServiceType, Service, FoodService, ServiceProviderApplication, FavoriteService,FoodTypeService,
FoodType, FoodServiceFood, Food, DJService, Venue, PhotoGrapherService, EntertainementService, DecorationService,
Decor, DecorEventType, ServiceReservation,Reservation)

from .serializers import (FoodServiceSerializer, ServiceTypeSerializer, ServiceProviderApplicationSerializer,
FavoriteServiceSerializer, ServiceSerializer, DJServiceSerializer, FoodTypeSerializer, FoodTypeServiceSerializer,
FoodSerializer, FoodServiceFoodSerializer, VenueSerializer, PhotoGrapherServiceSerializer
,EntertainementServiceSerializer, DecorationServiceSerializer, DecorSerializer,DecorEventTypeListSerializer,
MyServiceTypeSerializer, ServiceReservationSerializer
)

from wallet.models import FEE_PERCENTAGE,CenterWallet

from policy import get_refund_after_cancelling_service_reservation


def get_model_for_service_type(type):
    if type == 'food':
        return FoodService
    if type == 'DJservice':
        return DJService
    if type == 'venue':
        return Venue
    if type == 'photographer':
        return PhotoGrapherService
    if type == 'entertainment':
        return EntertainementService
    if type == 'decoration':
        return DecorationService     
    return None

def get_serializer_for_service_type(type):
    if type == 'food':
        return FoodServiceSerializer
    if type == 'DJservice':
        return DJServiceSerializer
    if type == 'venue':
        return VenueSerializer
    if type == 'photographer':
        return PhotoGrapherServiceSerializer
    if type == 'entertainment':
        return EntertainementServiceSerializer   
    if type == 'decoration':
        return DecorationServiceSerializer  
    return None


def inside_range(range_start,range_end,start,end):
    """
    Check if the line segment [start, end] is fully inside another line segment [range_start, range_end].

    Args:
        range_start (number): Start of the outer line segment.
        range_end (number): End of the outer line segment.
        start (number): Start of the inner line segment.
        end (number): End of the inner line segment.

    Returns:
        bool: True if the inner line segment [start, end] is within the outer line segment [range_start, range_end].
    """
    if range_start >= range_end or start >= end:
        return False
    
    if start >= range_start and start < range_end and end > range_start and end <= range_end:
        return True
    return False

# def inside_event_range(event_start, event_end, reservation_start, resvation_end):
#     """
#     Check if the reservation range is inside event range:

#     Args:
#         event_start (number): Start of the event
#         event_end (number): End of the event.
#         reservation_start (number): Start of the reservation.
#         resvation_end (number): End of the reservation.

#     Returns:
#         bool: True if the inner line segment [start, end] is within the outer line segment [range_start, range_end].
#     """
#     # event_start = event_start.total_seconds()
#     return inside_range(event_start, event_end, reservation_start, resvation_end)

# print(inside_event_range(datetime(2020,5,2,12,00,00),datetime(2020,5,2,14,00,00),datetime(2020,5,2,12,00,00),datetime(2020,5,2,15,00,00)))

class ServiceTypeViewSet(ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAdminUser]


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','creat']:
            self.permission_classes = [IsAdminUser]
        elif self.action in['list']:
            self.permission_classes = [IsAuthenticated]
        else:
            pass
        return super().get_permissions()

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
        applicatoin_serializer = ServiceProviderApplicationSerializer(data=request.data, context={'request': request})
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
            return [IsOwnerOrAdminUser()]
        elif self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
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
        application = get_object_or_404(ServiceProviderApplication,id=pk)
        application.status = 'Approved'
        user = application.user
        user.is_service_provider = True
        application.save()
        user.save()

        if not application.service_type:
            return Response({'message':'you should provide a valid type for service'},status=status.HTTP_400_BAD_REQUEST)
       
        model = get_model_for_service_type(application.service_type.type) 
        service,created = model.objects.get_or_create(
            service_provider = user,
            name = application.name,
            service_type = application.service_type,
            phone = application.phone,
            location = application.location
        )
        service.save()
        return Response({'message':'approved'},status= status.HTTP_200_OK)

    
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
            return serializer
        elif self.action in ['retrieve','update','partial_update']:
            pk = self.kwargs.get('pk')
            service = get_object_or_404(Service,id = pk)    
        return get_serializer_for_service_type(service.service_type.type)

    def get_object(self):
        # Override get_object to return the correct subclass instance
        obj = super().get_object()
        return self.get_subclass_instance(obj.id)

    def get_subclass_instance(self, pk):
        service = get_object_or_404(Service, pk=pk)
        model = get_model_for_service_type(service.service_type.type)
        sub_service = model.objects.get(id = service.id)
        return sub_service
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsServiceOwnerOrAdmin]
        elif self.action in['create']:
            self.permission_classes = [IsAdminUser]
        elif self.action in['list','retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            pass
        return super().get_permissions()
    

class MyServiceAPIView(APIView):
    def get(self,requset,**kwargs):
        user = requset.user
        service = Service.objects.filter(service_provider = user).first()
        model = get_model_for_service_type(service.service_type.type)
        service = model.objects.filter(service_provider = user).first()
        serializer = get_serializer_for_service_type(service.service_type.type)
        print(serializer)
        serializer = serializer(service)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MyServiceTypeAPIView(APIView):

    def get(self,requset,**kwargs):
        user = requset.user
        service = Service.objects.filter(service_provider = user).first()
        serializer = MyServiceTypeSerializer({'service_id': service.id,
                                               'type' : service.service_type.type,
                                               'type_id': service.service_type.id,
                                               'avg_rating':service.avg_rating} )
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class FoodTypeAPIView(APIView):

    def post(self,requset,service_pk,**kwargs):
        service = get_object_or_404(FoodService,id = service_pk)
        user = requset.user
        serialzer = FoodTypeSerializer(data = requset.data)
        if serialzer.is_valid():
            type,created = FoodType.objects.get_or_create(type = serialzer.validated_data['type'])
            print(type)
            food_type_service,created = FoodTypeService.objects.get_or_create(foodService = service,foodType=type)
            food_type_service.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors)
    

    def get(self,requset,service_pk,**kwargs):
        food_service = FoodService.objects.get(id = service_pk)
        types_of_food = FoodTypeService.objects.filter(foodService = food_service).all()
        print(types_of_food)
        serialzer = FoodTypeServiceSerializer(types_of_food,many = True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwnerOrAdmin()] 
        

class DeleteRetrieveFoodTypeAPIView(APIView):

    def delete(self, request, service_pk, type_pk,**kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        
        if not type_pk:
            return Response({'detail': 'Type is required to delete.'}, status=status.HTTP_400_BAD_REQUEST)

        type_instance = get_object_or_404(FoodType, id=type_pk)
        food_type_service = get_object_or_404(FoodTypeService, foodService=service, foodType=type_instance)

        food_type_service.delete()
        return Response({'detail': 'Food type deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, service_pk, type_pk,**kwargs):
        food_type = get_object_or_404(FoodType,id = type_pk)
        serialzer = FoodTypeSerializer(food_type)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()] 
    

class FoodAPIView(APIView):
    
    def post(self, request, service_pk, type_pk, **kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        food_type = get_object_or_404(FoodType, id=type_pk)
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            food, created = Food.objects.get_or_create(
                food_type=food_type,
                name=serializer.validated_data['name'],
                price =  serializer.validated_data['price'],
                ingredients = serializer.validated_data.get('ingredients','')
                # defaults={'ingredients' : serializer.validated_data.get('ingredients','')}
            )
            FoodServiceFood.objects.create(foodService=service, food=food)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_pk,type_pk = None, food_pk=None, **kwargs):
        if food_pk:
            food = get_object_or_404(Food,id = food_pk)
            serializer = FoodSerializer(food)
            return Response(serializer.data, status=status.HTTP_200_OK)            
        service = get_object_or_404(FoodService, id=service_pk)
        food_type = get_object_or_404(FoodType, id=type_pk)
        foods = FoodServiceFood.objects.filter(foodService=service,food__food_type=food_type)
        serializer = FoodServiceFoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, service_pk, food_pk, **kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        food_service_food = get_object_or_404(FoodServiceFood, foodService=service, food_id=food_pk)
        food_service_food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['DELETE', 'POST']:
            return [IsServiceOwnerOrAdmin()] 
    

class ListRetrieveFoodAPIView(APIView):
    def get(self, request, service_pk, food_pk=None, **kwargs):

        food_type_ids = request.query_params.getlist('food_type')
        service = get_object_or_404(FoodService, id=service_pk)
        if food_pk:
            food = get_object_or_404(Food,id = food_pk)
            try:
                food = FoodServiceFood.objects.get(foodService=service,food = food)
            except FoodServiceFood.DoesNotExist:
                return Response({'message':'this service does not have such food'},status=404)
            serializer = FoodSerializer(food)
            return Response(serializer.data, status=status.HTTP_200_OK)         
        foods = FoodServiceFood.objects.filter(foodService=service)
        if food_type_ids:
            foods = foods.filter(food__food_type__in = food_type_ids).distinct()   
        serializer = FoodServiceFoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LocationDetailView(RetrieveUpdateAPIView):
    serializer_class = LocationSerializer

    def get_object(self):
        service_pk = self.kwargs.get('service_pk')
        service = get_object_or_404(Service,pk = service_pk)
        if not service.location:
            raise Location.DoesNotExist("Location not found for this service.")
        return service.location


    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        if self.request.method in ['PUT','PATCH']:
            self.permission_classes = [IsServiceOwnerOrAdmin]
        return super().get_permissions()

class DecorAPIView(APIView):

    def post(self, request, service_pk, **kwargs):
        service = get_object_or_404(DecorationService, id=service_pk)
        decorSerializer = DecorSerializer(data=request.data)
        decor_event_types_list_serializer = DecorEventTypeListSerializer(data=request.data)
        if decorSerializer.is_valid():
            if decor_event_types_list_serializer.is_valid():
                decor,created = Decor.objects.get_or_create(
                        decor_service = service,
                        name = decorSerializer.validated_data['name'],
                        quantity  = decorSerializer.validated_data['quantity'],
                        hourly_rate = decorSerializer.validated_data.get('hourly_rate',0.00),
                        price = decorSerializer.validated_data.get('price',0.00),
                        description = decorSerializer.validated_data.get('description',''),
                )
                decor_event_types = ast.literal_eval(decor_event_types_list_serializer.validated_data.get('decor_event_types')[0])
                for event_type in decor_event_types:
                    event_type = get_object_or_404(EventType,id = event_type)
                    DecorEventType.objects.get_or_create(decor = decor, event_type = event_type)
                return Response(DecorSerializer(decor).data, status=status.HTTP_201_CREATED)
            return Response(decor_event_types_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(decorSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, service_pk, decor_pk=None, **kwargs):
        event_type_ids = request.query_params.getlist('event_type')

        if decor_pk:
            decor = get_object_or_404(Decor, id=decor_pk)
            serializer = DecorSerializer(decor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        service = get_object_or_404(DecorationService, id=service_pk)
        decors = Decor.objects.filter(decor_service=service)

        if event_type_ids:
            decors = decors.filter(decoreventtype__event_type__in=event_type_ids).distinct()

        serializer = DecorSerializer(decors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, service_pk, decor_pk, **kwargs):
        service = get_object_or_404(DecorationService, id=service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service=service)
        decor_event_types_list_serializer = DecorEventTypeListSerializer(data=request.data, partial = True)
        decor_serializer = DecorSerializer(decor, data=request.data, partial=True)
        if decor_event_types_list_serializer.is_valid():
            if decor_event_types_list_serializer.validated_data.get('decor_event_types') is not None:
                DecorEventType.objects.filter(decor = decor).all().delete()
                decor_event_types = ast.literal_eval(decor_event_types_list_serializer.validated_data.get('decor_event_types')[0])
                for event_type in decor_event_types:
                    event_type = get_object_or_404(EventType,id = event_type)
                    DecorEventType.objects.get_or_create(decor = decor, event_type = event_type)

            if decor_serializer.is_valid():
                decor_serializer.save()
                return Response(decor_serializer.data, status=status.HTTP_200_OK)
            return Response(decor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(decor_event_types_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, service_pk, decor_pk, **kwargs):
        service = get_object_or_404(DecorationService, id=service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service=service)
        decor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['DELETE', 'POST', 'PUT', 'PATCH']:
            return [IsServiceOwnerOrAdmin()] 
    

class ServiceReservationAPIView(APIView):
    def get(self, request, service_pk, reservation_pk=None):
        # Retrieve the service
        service = get_object_or_404(Service, id=service_pk)
        service_type = service.service_type.type
        
        if reservation_pk is not None:
            # Retrieve a specific reservation
            reservation = get_object_or_404(ServiceReservation, id=reservation_pk, service=service)
            serializer = ServiceReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reservations = ServiceReservation.objects.filter(service=service)
            serializer = ServiceReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request, service_pk,reservation_pk=None):
        service = get_object_or_404(Service,id = service_pk)
        service_type = service.service_type.type
        if service_type in ['food', 'decoration']:
            return Response({"error": "Cannot reserve services of type 'food' or 'decoration'"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceReservationSerializer(data = request.data)
        if serializer.is_valid():
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')
            event = serializer.validated_data.get('event')
            if event.user != request.user:
                return Response({'message':'you do not own this event'}, status = status.HTTP_400_BAD_REQUEST)
            # check if it is in the event time range
            is_inside = inside_range(event.start_time,event.end_time,start_time,end_time)
            if not is_inside:
                return Response({'message':'make sure that start time is smaller than end time or the reservation range is inside the event range'},status=status.HTTP_400_BAD_REQUEST)
            model = get_model_for_service_type(service_type)
            service = model.objects.get(id = service_pk)
            print(service.hourly_rate)
            duration = (end_time - start_time).total_seconds() / 3600
            cost = float(service.hourly_rate) * duration 
            if cost + cost * FEE_PERCENTAGE >= request.user.get_wallet().balance:
                return Response({'messgae':'insuficient funds'},status=status.HTTP_400_BAD_REQUEST)
            service_reservation = serializer.save(service = service,cost = cost)
            request.user.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = cost, reservation = service_reservation)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # def delete(self, request, service_pk,reservation_pk=None):
    #     reservation = get_object_or_404(ServiceReservation, id = reservation_pk)
    #     # reservation_owner = reservation.event.user
    #     print(request.user.is_superuser)
    #     if reservation.event.user == request.user or request.user.is_superuser:
    #         reservation.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     print('m')
    #     return Response({'message':'you do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [DefaultOrIsAdminUser()]
        elif self.request.method == 'DELETE':
            return [DefaultOrIsAdminUser()] 
        

class RejectServiceReservationAPIView(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        reservation = get_object_or_404(ServiceReservation, id = reservation_pk)
        if request.user == reservation.service.service_provider:
            reservation.status = 'Rejected'
            reservation_cost = float(reservation.cost) 
            fee = reservation_cost* FEE_PERCENTAGE
            CenterWallet.objects.first().transfer_funds( reservation.event.user.get_wallet(),amount=reservation_cost+fee,reservation=reservation)   
            reservation.save()
            return Response({'message':'the reservation has been rejected successfully'}, status= 200)  
        else:
            raise PermissionDenied('you do not have permission to perform this action')


class ConfirmReservaiton(APIView):
    # when service provider confirm 
    # service_provider.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = cost * 0.5, reservation = service_reservation)
    pass