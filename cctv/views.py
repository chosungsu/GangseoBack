from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, action
from .models import Count, Map
from .serializers import CountSerializer, MapSerializer
from django.http import JsonResponse
from django.views.generic import View
from . import modelfile as mf

# Create your views here.
@api_view(['GET', 'DELETE'])
def Getcounts(request, pk) :
    result = Count.objects.all()
    
    if (request.method == 'GET') :
        mf.getdong(pk)
        serializer = CountSerializer(result, many=True)
        return Response(serializer.data)
    else :
        result.delete()
        return Response(serializer.data)
@api_view(['GET', 'DELETE', 'PUT', 'POST'])
def Getmapparameter(request, pk1, pk2) :
    try:
        result = Map.objects.get()
    except Map.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    mf.getdong(pk1)
    mf.clustering(pk2)
    if (request.method == 'GET') :
        result = Map.objects.all()
        serializer = MapSerializer(result, many=True)
        return Response(serializer.data)
    elif (request.method == 'POST') :
        data = request.data
        result = Map.objects.create(
            lat = data['lat'],
            lon = data['lon'],
            summary = data['summary'],
        )
        serializer = MapSerializer(result, many=True)
        return Response(serializer.data)
    else :
        result = Map.objects.all()
        result.delete()
        return Response(serializer.data)