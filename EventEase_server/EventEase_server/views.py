# views.py
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import os

class ProtectedMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, path, format=None):
        # Construct the full file path
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            raise Response("Media file not found")

        # Return the file as a response
        return FileResponse(open(file_path, 'rb'))
