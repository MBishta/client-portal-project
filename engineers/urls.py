from django.urls import path

from .views import engineer_list_view, engineer_detail_view, engineer_create_view

app_name = 'engineers'

urlpatterns = [
    path('', engineer_list_view, name='engineer_list'),
    path('add/', engineer_create_view, name='engineer_add'),
    path('<int:pk>/', engineer_detail_view, name='engineer_detail'),
]