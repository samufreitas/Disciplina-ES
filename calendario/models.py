from django.db import models

# Create your models here.
class Agendamento(models.Model):
    titulo = models.CharField(max_length=200)
    data = models.DateTimeField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()