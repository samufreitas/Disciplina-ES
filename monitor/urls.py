from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('', views.pag_monitor, name='pag_monitor'),
    path('agendar_monitor/', views.agendar_monitor, name='agendar_monitor'),
    path('lista_monitor/', views.listar_monitor, name='lista_monitor'),
    path('agendamentos/<int:agendamento_id>/delete/', views.excluir_agendamento, name='excluir_agendamento'),

]