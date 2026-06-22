from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Motorista(AbstractUser):
    modelo = models.CharField(max_length=50)
    consumo = models.FloatField()
    def __str__(self) -> str:
        return self.email

class Corrida(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    distancia = models.FloatField()
    valor_corrida = models.FloatField()
    lucro = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)
    
