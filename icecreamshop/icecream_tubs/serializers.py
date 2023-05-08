from rest_framework import serializers
from .models import Flavor, IceCreamTub


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = "__all__"


class IceCreamTubSerializer(serializers.ModelSerializer):
    flavor_name = serializers.CharField(source='flavor.name', read_only=True)
    class Meta:
        model = IceCreamTub
        fields = "__all__"
