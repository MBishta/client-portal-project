from django.urls import path

from .views import client_list_view

app_name = 'clients'

urlpatterns = [
    path('', client_list_view, name='client_list'),
]