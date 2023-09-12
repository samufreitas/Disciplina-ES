from django.contrib.auth.models import User
from django.db import models
from laboratorio.models import Laboratorio

class Tipo(models.Model):
    titulo = models.CharField(max_length=60)
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['id']

    def __str__(self):
        return self.titulo
# Create your models here.
class Agendamento(models.Model):
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=30)
    opicional = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data']

    def __str__(self):
        return self.titulo
