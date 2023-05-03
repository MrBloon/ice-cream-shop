from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def create(self, validated_data):
        order_pk = self.context.get("view").kwargs.get("order_pk")
        order = get_object_or_404(Order, pk=order_pk)
        validated_data["order"] = order
        order_item = super().create(validated_data)
        return order_item

    def validate(self, attrs):
        if attrs["scoops_requested"] > attrs["ice_cream_tub"].scoops_available:
            raise serializers.ValidationError(
                "Number of scoops_requested exceeds number of scoops available in ice cream tub."
            )

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("total_price", "order_number", "is_confirmed")
