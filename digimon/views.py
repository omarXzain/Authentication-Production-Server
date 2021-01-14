from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView

from .serializer import DigimonSerializer
from .models import Digimon
from .permissions import PermissionsClass

# Create your views here.
class DigimonListView(ListAPIView):
    queryset = Digimon.objects.all()
    serializer_class = DigimonSerializer
    permission_classes = (PermissionsClass,)

class DigimonDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Digimon.objects.all()
    serializer_class = DigimonSerializer
    permission_classes = (PermissionsClass,)