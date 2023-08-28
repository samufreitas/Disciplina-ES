# urls.py
from django.urls import path
from .views import UserUpdateView
from . import views
app_name = 'accounts'


urlpatterns = [
    path('create/', views.add_user, name='user_create'),
    path('list/', views.list_user, name='user_list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('exluir/<int:user_id>/', views.user_delete, name='user_delete'),
    path('login/', views.user_login, name='user_login'),
    path('sair/', views.user_logout, name='user_logout'),
    path('nova_senha/', views.user_new_password, name='user_new_password'),
    path('voltar/', views.voltar, name='voltar'),
]

