from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()