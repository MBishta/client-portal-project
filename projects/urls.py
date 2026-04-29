from django.urls import path

from .views import project_list_view, project_detail_view

app_name = 'projects'

urlpatterns = [
    path('', project_list_view, name='project_list'),
    path('<int:pk>/', project_detail_view, name='project_detail'),
]