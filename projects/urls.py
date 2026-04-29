from django.urls import path

from .views import project_list_view

app_name = 'projects'

urlpatterns = [
    path('', project_list_view, name='project_list'),
]