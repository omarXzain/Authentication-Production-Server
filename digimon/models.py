from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Digimon(models.Model):
    Owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Digimon = models.CharField(max_length=64)
    Hp = models.CharField(max_length=64)
    Skill = models.TextField()

    def __str__(self):
        return self.Digimon