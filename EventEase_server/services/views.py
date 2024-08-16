import ast
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter
from accounts.permissions import IsAdminUser,IsOwner,IsOwnerOrAdminUser,IsServiceOwnerOrAdmin,Default,DefaultOrIsAdminUser
# from locations.serializers import LocationSerializer
from locations.models import Address, Location
from locations.serializers import AddressSerializer,LocationSerializer

from events.models import EventType, Event

from EventEase_server.utils import CustomPageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .models import (ServiceType, Service, FoodService, ServiceProviderApplication, FavoriteService,FoodTypeService,
FoodType, FoodServiceFood, Food, DJService, Venue, PhotoGrapherService, EntertainementService, DecorationService,
Decor, DecorEventType, ServiceReservation, Reservation, DecorsReservation, DecorsInReservation, FoodInOrder, Order)

from .serializers import (FoodServiceSerializer, ServiceTypeSerializer, ServiceProviderApplicationSerializer,
FavoriteServiceSerializer, ServiceSerializer, DJServiceSerializer, FoodTypeSerializer, FoodTypeServiceSerializer,
FoodSerializer, FoodServiceFoodSerializer, VenueSerializer, PhotoGrapherServiceSerializer
,EntertainementServiceSerializer, DecorationServiceSerializer, DecorSerializer,DecorEventTypeListSerializer,
MyServiceTypeSerializer, ServiceReservationSerializer, NewFoodTypeSerializer, DecorsReservationSerializer,
DecorsListSerializer, OrderSerializer, FoodsListSerializer)

from wallet.models import FEE_PERCENTAGE,CenterWallet

from policy import RESERVATION_PROTECTION_PERCENTAGE, get_refund_after_cancelling_reservation, get_refund_after_cancelling_order

from .filters import ServiceFilter

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
        status_param = request.query_params.get('status', None)
        if status_param:
            if status_param not in ['Pending', 'Approved', 'Rejected']:
                return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
            applications = applications.filter(status=status_param)
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(applications, request)
        serializer = ServiceProviderApplicationSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    
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
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filterset_class = ServiceFilter
    search_fields = ['name','description']
    

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

        type_instance.delete()
        food_type_service.delete()
        return Response({'detail': 'Food type deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, service_pk, type_pk,**kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        food_type = get_object_or_404(FoodType, id=type_pk)
        food_type_service = get_object_or_404(FoodTypeService,foodService = service, foodType=food_type)
        serialzer = FoodTypeSerializer(food_type_service.foodType)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()] 
    

class FoodAPIView(APIView):
    
    # maybe utilizing get_queryset is better 
    #               |
    #               V
    # def get_queryset(self, service_pk, food_type_pk, food_pk=None):
    #     # Base queryset for FoodServiceFood
    #     queryset = FoodServiceFood.objects.filter(
    #         foodService_id=service_pk,
    #         food__food_type_id=food_type_pk
    #     )
    #     if food_pk:
    #         queryset = queryset.filter(food_id=food_pk)
    #     return queryset
    
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
        service = get_object_or_404(FoodService, id=service_pk)
        food_type = get_object_or_404(FoodType, id=type_pk)
        if food_pk:
            food = get_object_or_404(Food,id = food_pk)
            try:
                food = FoodServiceFood.objects.get(foodService=service,food__food_type=food_type,food=food)
            except FoodServiceFood.DoesNotExist:
                return Response({'message':'the service do not have such food'},status=400)
            serializer = FoodServiceFoodSerializer(food)
            return Response(serializer.data, status=status.HTTP_200_OK)            
        foods = FoodServiceFood.objects.filter(foodService=service,food__food_type=food_type).order_by('food__price')
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(foods, request)
        serializer = FoodServiceFoodSerializer(paginated_queryset , many=True)
        return paginator.get_paginated_response(serializer.data) 
    
    def delete(self, request, service_pk, food_pk, **kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        food_service_food = get_object_or_404(FoodServiceFood, foodService=service, food_id=food_pk)
        food_service_food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, service_pk,type_pk = None, food_pk=None, **kwargs):
        service = get_object_or_404(FoodService, id=service_pk)
        food_type = get_object_or_404(FoodType, id=type_pk)
        food_service_food = get_object_or_404(FoodServiceFood, foodService=service, food_id=food_pk, food__food_type =food_type)
        new_food_type_serializer = NewFoodTypeSerializer(data=request.data)
        if new_food_type_serializer.is_valid():
            new_type = new_food_type_serializer.validated_data['new_type']
            new_type = get_object_or_404(FoodType,id = new_type)
            food_service_food.food.food_type = new_type
        serializer = FoodSerializer(food_service_food.food,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['DELETE', 'POST', 'PATCH']:
            return [IsServiceOwnerOrAdmin()] 
    

class ListRetrieveFoodAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, service_pk, food_pk=None, **kwargs):

        food_type_ids = request.query_params.getlist('food_type')
        service = get_object_or_404(FoodService, id=service_pk)
        if food_pk:
            food = get_object_or_404(Food,id = food_pk)
            try:
                food = FoodServiceFood.objects.get(foodService=service,food = food)
            except FoodServiceFood.DoesNotExist:
                return Response({'message':'this service does not have such food'},status=404)
            serializer = FoodServiceFoodSerializer(food)
            return Response(serializer.data, status=status.HTTP_200_OK)
          
        foods = FoodServiceFood.objects.filter(foodService=service)
                # Get search query parameter
        search_query = request.query_params.get('search', '')
        if search_query:
            foods = foods.filter(
                Q(food__name__icontains=search_query) |  # Example: search by food name
                Q(food__ingredients__icontains=search_query)  # Example: search by food ingredients
            )       
        
        if food_type_ids:
            foods = foods.filter(food__food_type__in = food_type_ids).distinct()
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(foods, request)
        serializer = FoodServiceFoodSerializer(paginated_queryset , many=True)
        return paginator.get_paginated_response(serializer.data)    

    




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
        service = get_object_or_404(DecorationService, id=service_pk)
        if decor_pk:
            decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
            serializer = DecorSerializer(decor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        decors = Decor.objects.filter(decor_service=service)
        search_query = request.query_params.get('search', '')
        if search_query:
            decors = decors.filter(
                Q(name__icontains=search_query) |  # Example: search by decor name
                Q(description__icontains=search_query)  # Example: search by decor description
            )    
        if event_type_ids:
            decors = decors.filter(decoreventtype__event_type__in=event_type_ids).distinct()
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(decors, request)
        serializer = DecorSerializer(paginated_queryset , many=True)
        return paginator.get_paginated_response(serializer.data)   
    
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
            if request.user == service.service_provider:
                reservation = ServiceReservation.objects.filter(service=service)
            else :
                reservations = ServiceReservation.objects.filter(service=service, event__user = request.user)
            status_param = request.query_params.get('status', None)
            if status_param:
                reservations = reservations.filter(status=status_param)
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(reservations, request)
            serializer = ServiceReservationSerializer(paginated_queryset , many=True)
            return paginator.get_paginated_response(serializer.data)    

        

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
            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                service=service
            ).filter(
                Q(start_time__lt=start_time, end_time__gt=start_time) |
                Q(start_time__gt=start_time, start_time__lt=end_time)
            )
            if overlapping_reservations.exists():
                raise ValidationError("This service is already reserved during the selected time frame.")
        
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
    #     if reservation.event.user == request.user:
    #         if reservation.status == 'Pending'
    #         reservation.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response({'message':'you do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        if self.request.method in ['POST', 'GET']:
            return [DefaultOrIsAdminUser()]
        elif self.request.method == 'DELETE':
            return [DefaultOrIsAdminUser()] 
        

class ServicesReservationsAPIView(APIView):
    """
    return the reservatoins that user has made for specific services
    """
    def get(self,request):
        reservations = ServiceReservation.objects.filter(event__user = request.user).all()
        serializer = ServiceReservationSerializer(reservations, many = True)
        return Response(serializer.data,status=200)


class DecorsReservationsAPIView(APIView):
    def get(self,request):
        reservations = DecorsReservation.objects.filter(event__user = request.user).all()
        serializer = DecorsReservationSerializer(reservations, many = True)
        return Response(serializer.data,status=200)  
    


class ListOrdersAPIview(APIView):
    def get(self,request):
        reservations = Order.objects.filter(event__user = request.user).all()
        serializer = OrderSerializer(reservations, many = True)
        return Response(serializer.data,status=200) 
    


class RejectServiceReservationAPIView(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(ServiceReservation, id = reservation_pk, service = service)
        if request.user == reservation.service.service_provider:
            if reservation.status == 'Pending':
                reservation.status = 'Rejected'
                reservation_cost = float(reservation.cost) 
                fee = reservation_cost* FEE_PERCENTAGE
                CenterWallet.objects.first().transfer_funds( reservation.event.user.get_wallet(),amount=reservation_cost+fee,reservation=reservation)   
                reservation.save()
                return Response({'message':'the reservation has been rejected successfully'}, status= 200) 
            else:
                return Response({'message':'you can not reject this reservation'}, status= 400) 
        else:
            raise PermissionDenied('you do not have permission to perform this action')


class ConfirmServiceReservationAPIView(APIView):
    # when service provider confirm 
    # service_provider.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = cost * 0.5, reservation = service_reservation)
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(ServiceReservation, id = reservation_pk)
        if request.user == reservation.service.service_provider:
            if reservation.status == 'Pending':
                reservation.status = 'Confirmed'
                if  float(reservation.cost) * RESERVATION_PROTECTION_PERCENTAGE < request.user.get_wallet().balance:
                    request.user.get_wallet().transfer_funds(CenterWallet.objects.first(),
                                                            amount = float(reservation.cost) * RESERVATION_PROTECTION_PERCENTAGE,
                                                            reservation = reservation)
                    reservation.save()
                    return Response({'message':'the reservation has been confirmed successfully'}, status= 200)
                return Response({'message':'Insufficient funds'}, status= 400)
            else: return Response({'message':'you can not confirm this reservation'}, status= 400)
        else:
            raise PermissionDenied('you do not have permission to perform this action')
        

class CancelServiceReservation(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(ServiceReservation, id = reservation_pk)
        reservation_cost = float(reservation.cost)
        compensation,refund = get_refund_after_cancelling_reservation(request.user, reservation)
        if reservation.status != 'Confirmed':
            return Response({'message':'you can not cancel this reservation'}, status= 400)
        if request.user == reservation.service.service_provider:
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.event.user.get_wallet(),
                                                        amount=refund,
                                                        reservation=reservation)
            # we will return the fee to the service provider + the amount of money left after compensation
            #the remaining_money_after_compensation is the whole amount of money paid for compensation - the money that actually been paid as compensation
            remaining_money_after_compensation = reservation_cost*RESERVATION_PROTECTION_PERCENTAGE - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.service.service_provider.get_wallet(),
                                                        amount=reservation_cost*RESERVATION_PROTECTION_PERCENTAGE*FEE_PERCENTAGE + remaining_money_after_compensation,
                                                        reservation=reservation)
            reservation.status = 'Cancelled'  
            reservation.save()   
            return Response({'message':'the reservation has been cancelled successfully'}, status= 200)
        elif request.user == reservation.event.user:
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.service.service_provider.get_wallet(),
                                                        amount=refund,
                                                        reservation=reservation)
            # we will return the fee to the user
            remaining_money_after_compensation = reservation_cost - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.event.user.get_wallet(),
                                                        amount=reservation_cost*FEE_PERCENTAGE + remaining_money_after_compensation, # if compensation is zero then the user will get all money back
                                                        reservation=reservation)
            reservation.status = 'Cancelled'  
            reservation.save()   
            return Response({'message':'the reservation has been cancelled successfully'}, status= 200)
        else:
            return Response({'message':'you can not perform this actino'}, status= 401)        


class PayServiceReservation(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service,id=service_pk)
        reservation = get_object_or_404(ServiceReservation,id=reservation_pk)
        if service.service_type.type != 'decor':
            return Response({'message':'the service shoud be decor service'},status=400)
        if request.user != reservation.event.user:
            return Response({'message':'you don not own this reservation'}, status=400)
        CenterWallet.objects.first().transfer_funds(target_wallet=reservation.service.service_provider.get_wallet(),
                                                    amount=float(reservation.cost)+float(reservation.cost)*RESERVATION_PROTECTION_PERCENTAGE,
                                                    reservation=reservation)
        reservation.status = 'Paid'
        reservation.save()
        reservation.event.compute_total_cost()
        return Response({'message':f'reservation {reservation.id} paid successfully'},status=200)
            

class DecorsReservationAPIView(APIView):
    def post(self, request, service_pk):
        
        decor_service = get_object_or_404(DecorationService, id = service_pk)
        # Parse and validate the incoming data
        decor_list_serializer = DecorsListSerializer(data=request.data)
        decor_resrevation_serializer = DecorsReservationSerializer(data=request.data)
        if decor_resrevation_serializer.is_valid():
            start_time = decor_resrevation_serializer.validated_data.get('start_time')
            end_time = decor_resrevation_serializer.validated_data.get('end_time')
            event=decor_resrevation_serializer.validated_data.get('event')
            if request.user != event.user:
                return Response({'message':'you do not own this event'},status=401)
            #  save reservation data
            decors_reservation ,created= DecorsReservation.objects.get_or_create(event = event,
                                                    decor_service = decor_service,
                                                    start_time=start_time,
                                                    end_time=end_time,
                                                    cost=0
                                                    )
            #validating the decors in reservation data
            if decor_list_serializer.is_valid():
                decors_data = decor_list_serializer.validated_data['decors']

                # Process each item in the list
                processed_data = []
                for item in decors_data:
                    decor_id = item['decor_id']
                    quantity = item['quantity']
                    decor = get_object_or_404(Decor,id=decor_id)
                    if quantity > decor.quantity:
                        return Response({'message':'there is no enough qunatity'},status=400)
                    decors_in_reservation,created = DecorsInReservation.objects.get_or_create(decors_reservation = decors_reservation,
                                                                                    decor=decor,
                                                                                    quantity=quantity,
                                                                                    start_time=start_time,
                                                                                    end_time=end_time,
                                                                                    price = float(decor.hourly_rate)*((end_time-start_time).total_seconds() / 3600)*quantity)
                    decors_reservation.cost = float(decors_reservation.cost) + decors_in_reservation.price
                    decors_reservation.save()
                    processed_data.append([decor_id, quantity])
                request.user.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = float(decors_reservation.cost ), reservation = decors_reservation)
                # Respond with processed data
                return Response(processed_data, status=status.HTTP_200_OK)
            else:
                return Response(decor_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: return Response(decor_resrevation_serializer.errors)


    def get(self, request, service_pk, reservation_pk=None):
        # Retrieve the service
        service = get_object_or_404(Service, id=service_pk)
        print(request.user)
        print(service.service_provider)
        if reservation_pk is not None:
            # Retrieve a specific reservation
            reservation = get_object_or_404(DecorsReservation, id=reservation_pk, decor_service=service)
            serializer = DecorsReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if request.user == service.service_provider:
                reservations = DecorsReservation.objects.filter(decor_service=service)
            else :
                reservations = DecorsReservation.objects.filter(decor_service=service, event__user = request.user)
            status_param = request.query_params.get('status', None)
            if status_param:
                reservations = reservations.filter(status=status_param)
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(reservations, request)
            serializer = ServiceReservationSerializer(paginated_queryset , many=True)
            return paginator.get_paginated_response(serializer.data) 

  
class RejectDecorsServiceReservationAPIView(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(DecorsReservation, id = reservation_pk, decor_service = service)
        if request.user == reservation.decor_service.service_provider:
            if reservation.status == 'Pending':
                reservation.status = 'Rejected'
                reservation_cost = float(reservation.cost) 
                fee = reservation_cost* FEE_PERCENTAGE
                CenterWallet.objects.first().transfer_funds( reservation.event.user.get_wallet(),amount=reservation_cost+fee,reservation=reservation)   
                reservation.save()
                return Response({'message':'the reservation has been rejected successfully'}, status= 200) 
            else:
                return Response({'message':'you can not reject this reservation'}, status= 400) 
        else:
            raise PermissionDenied('you do not have permission to perform this action')
        

class ConfirmDecorsServiceReservationAPIView(APIView):
    # when service provider confirm 
    # service_provider.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = cost * 0.5, reservation = service_reservation)
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(DecorsReservation, id = reservation_pk)
        if request.user == reservation.decor_service.service_provider:
            if reservation.status == 'Pending':
                reservation.status = 'Confirmed'
                if  float(reservation.cost) * RESERVATION_PROTECTION_PERCENTAGE < request.user.get_wallet().balance:
                    request.user.get_wallet().transfer_funds(CenterWallet.objects.first(),
                                                            amount = float(reservation.cost) * RESERVATION_PROTECTION_PERCENTAGE,
                                                            reservation = reservation)
                    reservation.save()
                    return Response({'message':'the reservation has been confirmed successfully'}, status= 200)
                return Response({'message':'Insufficient funds'}, status= 400)
            else: return Response({'message':'you can not confirm this reservation'}, status= 400)
        else:
            raise PermissionDenied('you do not have permission to perform this action')
        

class CancelDecorsServiceReservation(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        reservation = get_object_or_404(DecorsReservation, id = reservation_pk)
        reservation_cost = float(reservation.cost)
        compensation,refund = get_refund_after_cancelling_reservation(request.user, reservation)
        if reservation.status != 'Confirmed':
            return Response({'message':'you can not cancel this reservation'}, status= 400)
        if request.user == reservation.decor_service.service_provider:
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.event.user.get_wallet(),
                                                        amount=refund,
                                                        reservation=reservation)
            # we will return the fee to the service provider + the amount of money left after compensation
            #the remaining_money_after_compensation is the whole amount of money paid for compensation - the money that actually been paid as compensation
            remaining_money_after_compensation = reservation_cost*RESERVATION_PROTECTION_PERCENTAGE - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.decor_service.service_provider.get_wallet(),
                                                        amount=reservation_cost*RESERVATION_PROTECTION_PERCENTAGE*FEE_PERCENTAGE + remaining_money_after_compensation,
                                                        reservation=reservation)
            reservation.status = 'Cancelled'  
            reservation.save()   
            return Response({'message':'the reservation has been cancelled successfully'}, status= 200)
        elif request.user == reservation.event.user:
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.decor_service.service_provider.get_wallet(),
                                                        amount=refund,
                                                        reservation=reservation)
            # we will return the fee to the user
            remaining_money_after_compensation = reservation_cost - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=reservation.event.user.get_wallet(),
                                                        amount=reservation_cost*FEE_PERCENTAGE + remaining_money_after_compensation, # if compensation is zero then the user will get all money back
                                                        reservation=reservation)
            reservation.status = 'Cancelled'  
            reservation.save()   
            return Response({'message':'the reservation has been cancelled successfully'}, status= 200)
        else:
            return Response({'message':'you can not perform this actino'}, status= 401)
        

class PayDecorsServiceReservation(APIView):
    def post(self, request,service_pk=None, reservation_pk=None):
        service = get_object_or_404(Service,id=service_pk)
        reservation = get_object_or_404(DecorsReservation,id=reservation_pk)
        print(service.service_type.type)
        if service.service_type.type != 'decoration':
            return Response({'message':'the service shoud be decor service'},status=400)
        if request.user != reservation.event.user:
            return Response({'message':'you don not own this reservation'}, status=400)
        CenterWallet.objects.first().transfer_funds(target_wallet=reservation.decor_service.service_provider.get_wallet(),
                                                    amount=float(reservation.cost)+float(reservation.cost)*RESERVATION_PROTECTION_PERCENTAGE,
                                                    reservation=reservation)
        reservation.status = 'Paid'
        reservation.save()
        reservation.event.compute_total_cost()
        return Response({'message':f'reservation {reservation.id} paid successfully'},status=200)
        

class FoodOrderAPIView(APIView):
    def post(self, request, service_pk):
        service = get_object_or_404(Service, id=service_pk)
        if service.service_type.type != 'food':
            return Response({'message':'the service should be food'},status=400)
        if request.user == service.service_provider:
            return Response({'message':'you can not order food from your self'},status=400)
        order_serializer = OrderSerializer(data=request.data)
        food_list_serializer = FoodsListSerializer(data=request.data)
        
        if order_serializer.is_valid():
            total_price = 0
            event=order_serializer.validated_data.get('event')
            due_date=order_serializer.validated_data.get('due_date')
            if request.user != event.user:
                return Response({'message':'you do not own this event'},status=401)
            food_order = Order.objects.create(
                event=event,
                service=service,
                total_price=total_price,
                due_date = due_date,
                status='Pending'
            )
            
            if food_list_serializer.is_valid():
                foods_data = food_list_serializer.validated_data['foods']
                
                for item in foods_data:
                    food_id = item['food_id']
                    quantity = item['quantity']
                    food = get_object_or_404(Food, id=food_id)

                    price = float(food.price) * quantity
                    FoodInOrder.objects.create(
                        order=food_order,
                        food=food,
                        quantity=quantity,
                        price=price
                    )
                    
                    total_price += price
                
                food_order.total_price = total_price
                food_order.save()
                
                # Transfer funds from user's wallet to the service provider's wallet
                request.user.get_wallet().transfer_funds(
                    target_wallet=CenterWallet.objects.first(),
                    amount=total_price,
                    order=food_order
                )
                
                return Response({'message': 'Food order placed successfully', 'order_id': food_order.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(food_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, service_pk, order_pk=None):
        # Retrieve the service
        service = get_object_or_404(Service,id = service_pk)
        if service.service_type.type != 'food':
            return Response({'message':'no such service'},status=400)
        if order_pk is not None:
            order = get_object_or_404(Order, id=order_pk, service=service)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if request.user == service.service_provider:
                orders = Order.objects.filter(service=service)
            else :
                orders = Order.objects.filter(service=service, event__user = request.user)
            status_param = request.query_params.get('status', None)
            if status_param:
                orders = orders.filter(status=status_param)
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(orders, request)
            serializer = OrderSerializer(paginated_queryset , many=True)
            return paginator.get_paginated_response(serializer.data) 
class RejectFoodOrderAPIView(APIView):
    def post(self, request,service_pk=None, order_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        order = get_object_or_404(Order, id = order_pk, service = service)
        if request.user == order.service.service_provider:
            if order.status == 'Pending':
                order.status = 'Rejected'
                order_price = float(order.total_price) 
                fee = order_price* FEE_PERCENTAGE
                CenterWallet.objects.first().transfer_funds(target_wallet=order.event.user.get_wallet(),amount=order_price+fee,order=order)   
                order.save()
                return Response({'message':'the reservation has been rejected successfully'}, status= 200) 
            else:
                return Response({'message':'you can not reject this reservation'}, status= 400) 
        else:
            raise PermissionDenied('you do not have permission to perform this action')
        

class ConfirmFoodOrderAPIView(APIView):
    # when service provider confirm 
    # service_provider.get_wallet().transfer_funds(target_wallet = CenterWallet.objects.first(),amount = cost * 0.5, reservation = service_reservation)
    def post(self, request, service_pk=None, order_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        order = get_object_or_404(Order, id = order_pk)
        if request.user == order.service.service_provider:
            if order.status == 'Pending':
                order.status = 'Confirmed'
                if  float(order.total_price) * RESERVATION_PROTECTION_PERCENTAGE < request.user.get_wallet().balance:
                    request.user.get_wallet().transfer_funds(CenterWallet.objects.first(),
                                                            amount = float(order.total_price) * RESERVATION_PROTECTION_PERCENTAGE,
                                                            order = order)
                    order.save()
                    return Response({'message':'the order has been confirmed successfully'}, status= 200)
                return Response({'message':'Insufficient funds'}, status= 400)
            else: return Response({'message':'you can not confirm this order'}, status= 403)
        else:
            raise PermissionDenied('you do not have permission to perform this action')
        

class CancelFoodOrder(APIView):
    def post(self, request,service_pk=None, order_pk=None):
        service = get_object_or_404(Service, id = service_pk)
        order = get_object_or_404(Order, id = order_pk)
        order_price = float(order.total_price)
        compensation,refund = get_refund_after_cancelling_order(request.user, order)
        if order.status != 'Confirmed':
            return Response({'message':'you can not cancel this order'}, status= 400)
        if request.user == order.service.service_provider:
            CenterWallet.objects.first().transfer_funds(target_wallet=order.event.user.get_wallet(),
                                                        amount=refund,
                                                        order=order)
            # we will return the fee to the service provider + the amount of money left after compensation
            #the remaining_money_after_compensation is the whole amount of money paid for compensation - the money that actually been paid as compensation
            remaining_money_after_compensation = order_price*RESERVATION_PROTECTION_PERCENTAGE - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=order.service.service_provider.get_wallet(),
                                                        amount=order_price*RESERVATION_PROTECTION_PERCENTAGE*FEE_PERCENTAGE + remaining_money_after_compensation,
                                                        order=order)
            order.status = 'Cancelled'  
            order.save()   
            return Response({'message':'the order has been cancelled successfully'}, status= 200)
        elif request.user == order.event.user:
            CenterWallet.objects.first().transfer_funds(target_wallet=order.service.service_provider.get_wallet(),
                                                        amount=refund,
                                                        order=order)
            # we will return the fee to the user
            remaining_money_after_compensation = order_price - compensation
            CenterWallet.objects.first().transfer_funds(target_wallet=order.event.user.get_wallet(),
                                                        amount=order_price*FEE_PERCENTAGE + remaining_money_after_compensation, # if compensation is zero then the user will get all money back
                                                        order=order)
            order.status = 'Cancelled'  
            order.save()   
            return Response({'message':'the reservation has been cancelled successfully'}, status= 200)
        else:
            return Response({'message':'you can not perform this actino'}, status= 403)
        

class PayFoodOrder(APIView):
    def post(self, request,service_pk=None, order_pk=None):
        service = get_object_or_404(Service,id=service_pk)
        order = get_object_or_404(Order,id=order_pk)
        if service.service_type.type != 'food':
            return Response({'message':'the service shoud be food service'},status=400)
        if request.user != order.event.user:
            return Response({'message':'you don not own this order'}, status=400)
        CenterWallet.objects.first().transfer_funds(target_wallet=order.service.service_provider.get_wallet(),
                                                    amount=float(order.total_price)+float(order.total_price*RESERVATION_PROTECTION_PERCENTAGE),
                                                    order=order)
        order.status = 'Paid'
        order.save()
        order.event.compute_total_cost()
        return Response({'message':f'order {order.id} paid successfully'},status=200)