from django.urls import path

from .views import client_list_view, client_detail_view, client_create_view

app_name = 'clients'

urlpatterns = [
    path('', client_list_view, name='client_list'),
    path('add/', client_create_view, name='client_add'),
    path('<int:pk>/', client_detail_view, name='client_detail'),
]