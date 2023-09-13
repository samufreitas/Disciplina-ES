from django.urls import path
from . import views

app_name = 'secretaria'

urlpatterns = [
    path('', views.pag_secretaria, name='pag_secretaria'),
    path('agendar/', views.adicionar_evento, name='agendar'),

    path('exibir_modal/<int:agendamento_id>/', views.exibir_modal, name='exibir_modal'),
    path('eventos/', views.eventos, name='eventos'),
    path('lista/', views.listar_agendamentos, name='lista'),


    path('listar_solicitacao/', views.listar_solicitacao, name='listar_solicitacao'),
    path('conf_solicitacao/<int:agendamento_id>/update/', views.conf_solicitacao, name='conf_solicitacao'),
    path('agendamentos/<int:agendamento_id>/delete/', views.excluir_agendamento, name='excluir_agendamento'),
    path('agendamentos/<int:agendamento_id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('nega_solicitacao/<int:agendamento_id>/negar/', views.negar_solicitacao, name='negar_solicitacao'),
    path('add_tipo/', views.add_tipo, name='add_tipo'),
    path('list_tipo/', views.list_tipo, name='list_tipo'),
    path('excluir_tipo/<int:tipo_id>/delete/', views.excluir_tipo, name='excluir_tipo'),

]