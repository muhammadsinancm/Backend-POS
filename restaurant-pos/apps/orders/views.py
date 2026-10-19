from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsOwner
from apps.tables.models import Table
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]
    
    def get_queryset(self):
        queryset = (Order.objects.select_related("table", "created_by").prefetch_related("items"))
        user = self.request.user
        
        if user.is_superuser or user.role in ["owner", "cashier"]:
            return queryset

        if user.role == "waiter":
            return queryset.filter(created_by=user)

        if user.role == "kitchen":
            return queryset.filter(
                status__in=[
                    Order.Status.PLACED,
                    Order.Status.PREPARING,
                    Order.Status.READY,
                ]
            )
        
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsWaiter()]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response(
            OrderSerializer(order, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )
    
    @action(detail=True, methods=["post"], url_path="item-status")
    def update_item_status(self, request, pk=None):
        order = self.get_object()
        item_id = request.data.get("item_id")
        new_status = request.data.get("status")

        if not item_id or not new_status:
            raise ValidationError({
                "detail": "Both item_id and status are required."
            })

        user = request.user
        
        if user.is_superuser or user.role == "owner":
            allowed_statuses = {
                OrderItem.Status.PENDING,
                OrderItem.Status.PREPARING,
                OrderItem.Status.READY,
                OrderItem.Status.SERVED,
                OrderItem.Status.CANCELLED,
            }
        
        elif user.role == "kitchen":
            allowed_statuses = {
                OrderItem.Status.PREPARING,
                OrderItem.Status.READY,
            }
        elif user.role == "waiter":
            allowed_statuses = {OrderItem.Status.SERVED}
        else:
            raise PermissionDenied(
                "You cannot update order item statuses."
            )
        
        if new_status not in allowed_statuses:
            raise PermissionDenied(
                "Your role cannot set this item status."
            )
        
        with transaction.atomic():
            item = get_object_or_404(
                OrderItem.objects.select_for_update(),
                pk=item_id,
                order=order,
            )
        
            if user.role == "kitchen":
                if (
                    new_status == OrderItem.Status.PREPARING
                    and item.status != OrderItem.Status.PENDING
                ):
                    raise ValidationError(
                        "Only pending items can start preparation."
                    )
                
                if (
                    new_status == OrderItem.Status.READY
                    and item.status != OrderItem.Status.PREPARING
                ):
                    raise ValidationError(
                        "Only preparing items can be marked ready."
                    )
        
            if user.role == "waiter":
                if item.status != OrderItem.Status.READY:
                    raise ValidationError(
                        "Only ready items can be marked served."
                    )
        
            item.status = new_status
            item.save(update_fields=["status", "updated_at"])

            items = list(order.items.all())
        
            if items and all(
                entry.status == OrderItem.Status.CANCELLED
                for entry in items
            ):
                order.status = Order.Status.CANCELLED
        
            elif items and all(
                entry.status in [
                    OrderItem.Status.SERVED,
                    OrderItem.Status.CANCELLED,
                ]
                for entry in items
            ):
                order.status = Order.Status.SERVED
        
            elif items and all(
                entry.status in [
                    OrderItem.Status.READY,
                    OrderItem.Status.SERVED,
                    OrderItem.Status.CANCELLED,
                ]
                for entry in items
            ):
                order.status = Order.Status.READY
        
            elif any(
                entry.status == OrderItem.Status.PREPARING
                for entry in items
            ):
                order.status = Order.Status.PREPARING
        
            else:
                order.status = Order.Status.PLACED
        
            order.save(update_fields=["status", "updated_at"])
    
        order.refresh_from_db()
        
        return Response(
            OrderSerializer(order, context=self.get_serializer_context()).data
        )