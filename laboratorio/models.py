from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Laboratorio(models.Model):
    name = models.CharField(max_length=60)
    qt_maquinas = models.IntegerField(blank=False, null=False)  # blank= não obrigatorio/null=aceita valor nulo

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorio'
        ordering = ['id']

    # Retorna o nome da categoria
    def __str__(self):
        return self.name