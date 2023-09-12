from django.urls import path
from .views import LaboratorioCreateView,LaboratorioUpdateView
from . import views
app_name = 'laboratorio'

urlpatterns = [
    path('laboratorios/', views.list_lab, name='laboratorio_list'),
    path('laboratorios/create/', LaboratorioCreateView.as_view(), name='laboratorio_create'),
    path('laboratorios/<int:pk>/update/', LaboratorioUpdateView.as_view(), name='laboratorio_update'),
    path('excluir_lab/<int:lab_id>/delete/', views.excluir_lab, name='excluir_lab'),

]
