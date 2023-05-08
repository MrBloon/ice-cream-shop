from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


    @action(detail=True, methods=["patch"])
    def confirm(self, request, pk=None):
        order = self.get_object()

        if order.total_price == 0:
            raise serializers.ValidationError(
                "To confirm the order, add at least one item."
            )

        order.is_confirmed = True
        order.save()
        order.update_scoops_available_in_tubs()

        order_serializer = self.get_serializer(order)
        return Response(order_serializer.data)


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        print("request.data", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        order_id = self.kwargs.get("order_pk")
        queryset = OrderItem.objects.filter(order=order_id)

        return queryset
