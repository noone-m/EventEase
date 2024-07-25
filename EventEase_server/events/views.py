from rest_framework import viewsets
from .models import EventType
from .serializers import EventTypeSerializer
from accounts.permissions import IsAdminUser,IsAuthenticated

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','creat']:
            self.permission_classes = [IsAdminUser]
        elif self.action in['list','retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            pass
        return super().get_permissions()