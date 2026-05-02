from django.urls import path

from .views import (
    project_list_view,
    project_create_view,
    project_detail_view,
    project_file_edit_view,
    project_file_delete_view,
    project_comment_edit_view,
    project_comment_delete_view,
)

app_name = 'projects'

urlpatterns = [
    path('', project_list_view, name='project_list'),
    path('add/', project_create_view, name='project_add'),
    path('<int:pk>/', project_detail_view, name='project_detail'),

    path('files/<int:pk>/edit/', project_file_edit_view, name='project_file_edit'),
    path('files/<int:pk>/delete/', project_file_delete_view, name='project_file_delete'),

    path('comments/<int:pk>/edit/', project_comment_edit_view, name='project_comment_edit'),
    path('comments/<int:pk>/delete/', project_comment_delete_view, name='project_comment_delete'),
]