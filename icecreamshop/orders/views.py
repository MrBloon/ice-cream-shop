from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import OrderForm
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # for the same endpoint /orders we have two different methods
    #
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        context = {"orders": serializer.data}
        return render(request, "orders/list.html", context)

    def create(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect("orders-list")
        context = {"form": form}
        return render(request, "orders/create.html", context)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     context = {'orders': serializer.data}
    #     return render(request, 'orders/list.html', context)

    # def create(self, request, *args, **kwargs):
    #     form = OrderForm(request.POST or None)
    #     if request.method == 'POST':
    #         if form.is_valid():
    #             form.save()
    #             return redirect('orders-list')
    #     context = {'form': form}
    #     return render(request, 'orders/create.html', context)

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

    def get_queryset(self):
        order_id = self.kwargs.get("order_pk")
        queryset = OrderItem.objects.filter(order=order_id)

        return queryset
