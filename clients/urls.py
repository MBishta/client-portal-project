from django.urls import path

from .views import client_list_view, client_detail_view

app_name = 'clients'

urlpatterns = [
    path('', client_list_view, name='client_list'),
    path('<int:pk>/', client_detail_view, name='client_detail'),
]