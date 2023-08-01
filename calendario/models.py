from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from laboratorio.models import Laboratorio


# Create your models here.
class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('Agendado', 'Agendado'),
        ('Solicitado', 'Solicitado'),
    )
    titulo = models.CharField(max_length=200)
    data = models.DateTimeField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    opicional = RichTextField(null=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['id']

        # Retorna o nome da class Agendamento 

    def __str__(self):
        return self.titulo