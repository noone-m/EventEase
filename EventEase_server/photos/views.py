import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from services.models import Service,Decor,FoodType,FoodServiceFood
from accounts.permissions import IsServiceOwner, IsServiceOwnerOrAdmin
from . models import ServicePhotos,ServiceProfilePhoto,FoodPhotos,Food,MainFoodPhoto,DecorPhotos,MainDecorPhoto
from . serializers import (ServicePhotosSerializers,ServiceProfilePhotoSerialzer,FoodPhotosSerializers,
MainFoodPhotoSerializer, DecorPhotosSerializer, MainDecorPhotoSerializer)


class ServicePhotosAPIView(APIView):
    parser_classes = [MultiPartParser]
    def get(self,request,service_pk = None , photo_pk =None):
        if photo_pk:
            photo = get_object_or_404(ServicePhotos,id = photo_pk)
            serializer = ServicePhotosSerializers(photo)
            return Response(serializer.data)
        photos = ServicePhotos.objects.filter(service = service_pk)
        serializer = ServicePhotosSerializers(photos,many = True)
        return Response(serializer.data)
    
    def post(self,request,service_pk): 
        service = get_object_or_404(Service,id=service_pk)
        serializer = ServicePhotosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(service = service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,service_pk,photo_pk):
        print('delete')
        photo = get_object_or_404(ServicePhotos,id = photo_pk) 
        image_path = photo.image
        image_path = str(image_path)
        try:
            full_image_path = os.path.join(settings.MEDIA_ROOT,image_path)
            print(full_image_path)
            os.remove(full_image_path)
        except FileNotFoundError:
            pass
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwner()] 
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()] 

class ServiceProfilePhotoAPIView(APIView):
    def get(self, request, service_pk):
        service = get_object_or_404(Service,id = service_pk)
        profile_photo = get_object_or_404(ServiceProfilePhoto,service = service)
        serializer = ServiceProfilePhotoSerialzer(profile_photo)
        return Response(serializer.data)

    def post(self, request,service_pk):
        service = get_object_or_404(Service,id = service_pk)
        existing_profile_photo = ServiceProfilePhoto.objects.filter(service = service).first()
        if existing_profile_photo:
            return Response({'m':'there is already a  profile photo for the service'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceProfilePhotoSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save(service = service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, service_pk):
    #     service = get_object_or_404(Service, id = service_pk)
    #     profile_photo = ServiceProfilePhoto.objects.get(service = service)
    #     serializer = ServiceProfilePhotoSerialzer(profile_photo, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,service_pk):
        print('delete')
        service = get_object_or_404(Service,id = service_pk )
        photo = get_object_or_404(ServiceProfilePhoto,service = service) 
        image_path = photo.servicePhoto
        image_path = str(image_path)
        try:
            full_image_path = os.path.join(settings.MEDIA_ROOT,image_path)
            print(full_image_path)
            os.remove(full_image_path)
        except FileNotFoundError:
            pass
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['POST','PUT','DELETE']:
            return [IsServiceOwnerOrAdmin()] 
        

class FoodPhotosAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, service_pk, type_pk, food_pk, photo_pk=None):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        if photo_pk:
            photo = get_object_or_404(FoodPhotos, id=photo_pk, food=food_service_food.food)
            serializer = FoodPhotosSerializers(photo)
            return Response(serializer.data)
        photos = FoodPhotos.objects.filter(food=food_service_food.food)
        serializer = FoodPhotosSerializers(photos, many=True)
        return Response(serializer.data)

    def post(self, request, service_pk, type_pk, food_pk):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        print(food)
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        serializer = FoodPhotosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(food=food_service_food.food)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, type_pk, food_pk, photo_pk):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        photo = get_object_or_404(FoodPhotos, id=photo_pk)
        image_path = str(photo.image)
        try:
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            os.remove(full_image_path)
        except FileNotFoundError:
            pass
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwnerOrAdmin()]
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()]
        

class MainFoodPhotoAPIView(APIView):

    def get(self, request, service_pk, type_pk, food_pk):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        main_photo = get_object_or_404(MainFoodPhoto, food_id=food_pk)
        serializer = MainFoodPhotoSerializer(main_photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_pk, type_pk, food_pk):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        serializer = MainFoodPhotoSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data.get('foodPhoto'))
            food_photo = serializer.validated_data.get('foodPhoto')
            if food_service_food.food != food_photo.food: # if the photo that we're going to set main does not belong to the food
                return Response({'message':'the photo you chosed deos not belong to the corresponding food'},status=400)
            main_photo, created = MainFoodPhoto.objects.update_or_create(
                food=food_service_food.food,
                defaults={'foodPhoto': serializer.validated_data['foodPhoto']}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, type_pk, food_pk):
        service = get_object_or_404(Service,id = service_pk)
        food_type = get_object_or_404(FoodType, id = type_pk)
        food = get_object_or_404(Food, id=food_pk)
        food_service_food = FoodServiceFood.objects.filter(food=food, foodService = service, food__food_type = food_type).first()
        if food_service_food is None:
            return Response({'message':'no such food in this service'},status= 400)
        main_photo = get_object_or_404(MainFoodPhoto, food_id=food_pk)
        main_photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwnerOrAdmin()]
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()]
        
        
class DecorPhotosAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, service_pk, decor_pk, photo_pk=None):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service) 
        if photo_pk:
            photo = get_object_or_404(DecorPhotos, id=photo_pk, decor=decor)
            serializer = DecorPhotosSerializer(photo)
            return Response(serializer.data)
        photos = DecorPhotos.objects.filter(decor=decor)
        serializer = DecorPhotosSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, service_pk, decor_pk):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
        serializer = DecorPhotosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(decor=decor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, decor_pk, photo_pk):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
        photo = get_object_or_404(DecorPhotos, id=photo_pk)
        image_path = str(photo.image)
        try:
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            os.remove(full_image_path)
        except FileNotFoundError:
            pass
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwnerOrAdmin()]
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()]

class MainDecorPhotoAPIView(APIView):

    def get(self, request, service_pk, decor_pk):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
        main_photo = get_object_or_404(MainDecorPhoto, decor=decor)
        serializer = MainDecorPhotoSerializer(main_photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_pk, decor_pk):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
        serializer = MainDecorPhotoSerializer(data=request.data)
        if serializer.is_valid():
            decorPhoto = serializer.validated_data.get('decorPhoto')
            if decor != decorPhoto.decor: # if the photo that we're going to set main does not belong to the decor
                return Response({'message':'the photo you chosed deos not belong to the corresponding decor'},status=400)
            main_photo, created = MainDecorPhoto.objects.update_or_create(
                decor=decor,
                defaults={'decorPhoto': serializer.validated_data['decorPhoto']}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, decor_pk):
        service = get_object_or_404(Service,id = service_pk)
        decor = get_object_or_404(Decor, id=decor_pk, decor_service = service)
        main_photo = get_object_or_404(MainDecorPhoto, decor=decor)
        main_photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsServiceOwnerOrAdmin()]    
        elif self.request.method == 'DELETE':
            return [IsServiceOwnerOrAdmin()]