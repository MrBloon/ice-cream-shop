from rest_framework import routers

from .views import FlavorViewSet, IceCreamTubViewSet

icecreams_router = routers.DefaultRouter()
icecreams_router.register("flavors", viewset=FlavorViewSet, basename="flavors")
icecreams_router.register("icecream_tubs", viewset=IceCreamTubViewSet, basename="icecream_tubs")