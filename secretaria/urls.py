from django.urls import path
from . import views

app_name = 'secretaria'

urlpatterns = [
    path('', views.pag_secretaria, name='pag_secretaria'),
    path('agendar/', views.adicionar_evento, name='agendar'),
    path('eventos/', views.eventos, name='eventos'),
    path('lista/', views.listar_agendamentos, name='lista'),
    path('listar_solicitacao/', views.listar_solicitacao, name='listar_solicitacao'),
    path('conf_solicitacao/<int:agendamento_id>/update/', views.conf_solicitacao, name='conf_solicitacao'),
    path('agendamentos/<int:agendamento_id>/delete/', views.excluir_agendamento, name='excluir_agendamento'),

]