from django.contrib import admin
from django.urls import path, include


from .views import DigimonDetailsView, DigimonListView


urlpatterns = [
    path('', DigimonListView.as_view(), name='digimon'),
    path('<int:pk>/', DigimonDetailsView.as_view(), name='digimon_details'),
]