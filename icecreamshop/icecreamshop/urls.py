from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import routers

from icecream_tubs.views import FlavorViewSet, IceCreamTubViewSet
from orders.views import OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()

router.register(r"flavors", viewset=FlavorViewSet, basename="flavors")
router.register(r"icecream_tubs", viewset=IceCreamTubViewSet, basename="icecream_tubs")

router.register(r"orders", viewset=OrderViewSet, basename="orders")
router.register(
    r"orders/(?P<order_pk>[0-9]+)/order_items",
    viewset=OrderItemViewSet,
    basename="order_items",
)

urlpatterns = [
    # re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
