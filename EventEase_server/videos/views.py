import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from services.models import Service
from .models import Video
from .serializers import VideoSerializer

class VideoListCreateAPIView(APIView):
    def get(self, request, service_pk):
        service = get_object_or_404(Service,id = service_pk)
        videos = Video.objects.filter(service = service)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request, service_pk):
        service = get_object_or_404(Service,id = service_pk)
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service = service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoRetrieveDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'message':'video does not exist'}, status= status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_pk, video_pk):
        video = self.get_object(video_pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    def delete(self, request, service_pk, video_pk):
        video = self.get_object(video_pk)
        image_path = str(video.file)
        try:
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            os.remove(full_image_path)
        except FileNotFoundError:
            pass
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)