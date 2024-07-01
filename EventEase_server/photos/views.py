from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from services.models import Service
from . models import ServicePhotos
from . serializers import ServicePhotosSerializers


class ServicePhotosAPIView(APIView):
    parser_classes = [MultiPartParser]
    def get(self,request,pk):
        photos = ServicePhotos.objects.filter(service = pk)
        serializer = ServicePhotosSerializers(photos,many = True)
        return Response(serializer.data)
    
    def post(self,request,pk): 
        try:
            service = Service.objects.get(id = pk)
        except Service.DoesNotExist:
            return Response({'m':'service does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ServicePhotosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(service = service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)