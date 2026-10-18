from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters, viewsets
from apps.common.permission import IsOwnerOrReadOnly
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

class MenuPermissionTestView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, reqeust):
        return Response({
            "message": "You can view the menu."
        })
    
    def post(self, request):
        return Response({
            "message": "You can modify menu data."
        })
        
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    
    def get_queryset(self):
        queryset = Category.objects.all()

        if self.request.user.role != "owner" and not (
            self.request.user.is_superuser
        ):
            queryset = queryset.filter(is_active=True)

        return queryset

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["name", "price", "created_at"]
    ordering = ["category__name", "name"]

    def get_queryset(self):
        queryset = MenuItem.objects.select_related("category")

        if self.request.user.role != "owner" and not (self.request.user.is_superuser):
            queryset = queryset.filter(is_available=True,category__is_active=True)

        return queryset
