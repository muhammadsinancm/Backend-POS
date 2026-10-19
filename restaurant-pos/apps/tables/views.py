
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.permission import IsOwner

from .models import Table
from .serializers import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["number", "capacity"]
    ordering = ["number"]
    
    def get_queryset(self):
        queryset = Table.objects.all()

        if self.request.user.role != "owner" and not (
            self.request.user.is_superuser
        ):
            queryset = queryset.filter(is_active=True)

        return queryset
    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]

        return [permission() for permission in self.permission_classes]
