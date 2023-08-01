from django.urls import path
from . import views
from .views import AgendamentoCreateView

app_name = 'calendar'

urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('agende/', AgendamentoCreateView.as_view(), name='agenda'),
    path('agendar/', views.adicionar_evento, name='agendar'),
    path('eventos/', views.eventos, name='eventos'),
    path('lista/', views.listar_agendamentos, name='lista'),
    path('agendamentos/<int:agendamento_id>/excluir/', views.excluir_agendamento, name='excluir_agendamento'),
]
