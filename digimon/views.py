from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializer import DigimonSerializer
from .models import Digimon
from .permissions import PermissionsClass

# Create your views here.
class DigimonListView(ListAPIView, CreateAPIView):
    queryset = Digimon.objects.all()
    serializer_class = DigimonSerializer
    permission_classes = (PermissionsClass, IsAuthenticated)

class DigimonDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Digimon.objects.all()
    serializer_class = DigimonSerializer
    permission_classes = (PermissionsClass, IsAuthenticated)