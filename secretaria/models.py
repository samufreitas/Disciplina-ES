from django.contrib.auth.models import User
from django.db import models
from laboratorio.models import Laboratorio


# Create your models here.
class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('Agendado', 'Agendado'),
        ('Solicitado', 'Solicitado'),
    )
    TIPO_CHOICES = (
        ('Aula', 'Aula'),
        ('Monitoria', 'Monitoria'),
    )
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    opicional = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['id']

        # Retorna o nome da class Agendamento

    def __str__(self):
        return self.titulo