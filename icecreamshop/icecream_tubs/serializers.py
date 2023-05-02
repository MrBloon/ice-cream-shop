from rest_framework import serializers
from .models import Flavor, IceCreamTub


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = '__all__'


class IceCreamTubSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceCreamTub
        fields = '__all__'
