from rest_framework import serializers

from .models import Digimon

class DigimonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'Owner','Digimon', 'Hp', 'Skill')
        model = Digimon