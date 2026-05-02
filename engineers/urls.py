from django.urls import path

from .views import engineer_list_view

app_name = 'engineers'

urlpatterns = [
    path('', engineer_list_view, name='engineer_list'),
]