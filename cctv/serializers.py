from rest_framework import serializers
from .models import Count, Map

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Count
        fields = ('status', 'counts')
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('lat', 'lon', 'summary')