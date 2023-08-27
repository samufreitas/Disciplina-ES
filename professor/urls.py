from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.pag_professor, name='pag_professor'),
    path('agendar_professor/', views.agendar_professor, name='agendar_professor'),
    path('lista_professor/', views.listar_professor, name='listar_professor'),
    path('agendamentos/<int:agendamento_id>/delete/', views.excluir_agendamento, name='excluir_agendamento'),

]