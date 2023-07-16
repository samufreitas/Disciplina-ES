from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('agendar/', views.adicionar_evento, name='agendar'),
    path('eventos/', views.eventos, name='eventos'),
    path('lista/', views.listar_agendamentos, name='lista'),
    path('agendamentos/<int:agendamento_id>/excluir/', views.excluir_agendamento, name='excluir_agendamento'),
]
