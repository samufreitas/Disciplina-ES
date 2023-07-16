from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Laboratorio(models.Model):
    name = models.CharField(max_length=60)
    qt_monitor = models.IntegerField(blank=True, null=True)  # blank= não obrigatorio/null=aceita valor nulo
    qt_notebook = models.IntegerField(blank=True, null=True)
    qt_teclado = models.IntegerField(blank=True, null=True)
    qt_mouse = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorio'
        ordering = ['id']

    # Retorna o nome da categoria
    def __str__(self):
        return self.name