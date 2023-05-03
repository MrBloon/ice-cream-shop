from rest_framework import routers

from .views import OrderViewSet, OrderItemViewSet

orders_router = routers.DefaultRouter()
orders_router.register("orders", viewset=OrderViewSet, basename="orders")
orders_router.register("order_items", viewset=OrderItemViewSet, basename="order_items")
