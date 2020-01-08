from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import LocationsSerializer
from .models import Locations

class LocationsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer
