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
from services.models import Service
from accounts.permissions import IsServiceOwner, IsServiceOwnerOrAdmin
from . models import ServicePhotos,ServiceProfilePhoto,FoodPhotos,Food,MainFoodPhoto
from . serializers import ServicePhotosSerializers,ServiceProfilePhotoSerialzer,FoodPhotosSerializers,MainFoodPhotoSerializer


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
        profile_photo = ServiceProfilePhoto.objects.get(service = service)
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

    def put(self, request, service_pk):
        service = get_object_or_404(Service, id = service_pk)
        profile_photo = ServiceProfilePhoto.objects.get(service = service)
        serializer = ServiceProfilePhotoSerialzer(profile_photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self):
        # I will not implement delete here becauese we can just delete the photo
        # using DeleteServicePhotosAPIView and that in return will delete the 
        # whole record in data base
        pass

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['POST','PUT']:
            return [IsServiceOwnerOrAdmin()] 
        

class FoodPhotosAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, service_pk, type_pk, food_pk, photo_pk=None):
        food = get_object_or_404(Food, id=food_pk)
        if photo_pk:
            photo = get_object_or_404(FoodPhotos, id=photo_pk, food=food)
            serializer = FoodPhotosSerializers(photo)
            return Response(serializer.data)
        photos = FoodPhotos.objects.filter(food=food)
        serializer = FoodPhotosSerializers(photos, many=True)
        return Response(serializer.data)

    def post(self, request, service_pk, type_pk, food_pk):
        food = get_object_or_404(Food, id=food_pk)
        serializer = FoodPhotosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(food=food)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, type_pk, food_pk, photo_pk):
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
        main_photo = get_object_or_404(MainFoodPhoto, food_id=food_pk)
        serializer = MainFoodPhotoSerializer(main_photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_pk, type_pk, food_pk):
        food = get_object_or_404(Food, id=food_pk)
        serializer = MainFoodPhotoSerializer(data=request.data)
        if serializer.is_valid():
            main_photo, created = MainFoodPhoto.objects.update_or_create(
                food=food,
                defaults={'foodPhoto': serializer.validated_data['foodPhoto']}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, type_pk, food_pk):
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