from django.contrib import admin
from .models import Agendamento, Tipo
# Register your models here.

admin.site.register(Tipo)
admin.site.register(Agendamento)