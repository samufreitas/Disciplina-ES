# urls.py
from django.urls import path
from .views import UserUpdateView, UserDeleteView
from . import views
app_name = 'accounts'


urlpatterns = [
    path('create/', views.add_user, name='user_create'),
    path('list/', views.list_user, name='user_list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]

