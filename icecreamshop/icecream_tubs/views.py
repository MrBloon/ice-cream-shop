from rest_framework.viewsets import ModelViewSet

from .serializers import FlavorSerializer, IceCreamTubSerializer
from .models import Flavor, IceCreamTub


class FlavorViewSet(ModelViewSet):
    serializer_class = FlavorSerializer
    queryset = Flavor.objects.all()


class IceCreamTubViewSet(ModelViewSet):
    serializer_class = IceCreamTubSerializer
    queryset = IceCreamTub.objects.all()
