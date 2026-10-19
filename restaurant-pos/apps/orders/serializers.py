from rest_framework import serializers

from apps.menu.models import MenuItem
from apps.tables.models import Table
from .models import Order, OrderItem

class OrderItemInputSerializer(serializers.Serializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.filter(is_available=True, category__is_active=True))
    quantity = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=255)
    
class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            "id", "menu_item", "item_name", "unit_price", 
            "quantity", "line_total", "status", "notes", "created_at"
        ]
        read_only_fields = fields
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.IntegerField(
        source="table.number", read_only=True, allow_null=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    
    class Meta:
        model = Order
        fields = [
            "id", "order_number", "order_type", "table", "table_number", "created_by",
            "created_by_username", "status", "notes", "items", "created_at", "updated_at"
        ]
        read_only_fields = fields
        
class OrderCreateSerializer(serializers.Serializer):
    order_type = serializers.ChoiceField(
        choices=Order.OrderType.choices,
        default=Order.OrderType.DINE_IN,
    )
    table = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    items = OrderItemInputSerializer(many=True, allow_empty=False)
    
    def validate(self, attrs):
        order_type = attrs["order_type"]
        table = attrs.get("table")

        if order_type == Order.OrderType.DINE_IN and table is None:
            raise serializers.ValidationError({"table": "A table is required for dine-in orders."})
        
        if order_type == Order.OrderType.TAKEAWAY and table is not None:
            raise serializers.ValidationError({"table": "Takeaway orders must not have a table."})

        return attrs
    
    def create(self, validated_data):
        from uuid import uuid4
        from django.db import transaction

        items_data = validated_data.pop("items")
        table = validated_data.pop("table", None)
        request = self.context["request"]
        
        with transaction.atomic():
            if table is not None:
                table = Table.objects.select_for_update().get(pk=table.pk)

                if table.status != Table.Status.FREE:
                    raise serializers.ValidationError({"table": "This table is not free."})
            
            order = Order.objects.create(
                order_number=f"ORD-{uuid4().hex[:10].upper()}",
                table=table,
                created_by=request.user,
                **validated_data,
            )

            order_items = []
            
            for item_data in items_data:
                menu_item = item_data["menu_item"]

                order_items.append(
                    OrderItem(
                        order=order,
                        menu_item=menu_item,
                        item_name=menu_item.name,
                        unit_price=menu_item.price,
                        quantity=item_data["quantity"],
                        notes=item_data.get("notes", ""),
                    )
                )
                
            OrderItem.objects.bulk_create(order_items)
            
            if table is not None:
                table.status = Table.Status.OCCUPIED
                table.save(update_fields=["status", "updated_at"])

        return order