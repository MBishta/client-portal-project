from django.urls import path

from .views import (
    project_list_view,
    project_create_view,
    project_edit_view,
    project_delete_view,
    project_bulk_delete_view,
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
    path('bulk-delete/', project_bulk_delete_view, name='project_bulk_delete'),

    path('<int:pk>/', project_detail_view, name='project_detail'),
    path('<int:pk>/edit/', project_edit_view, name='project_edit'),
    path('<int:pk>/delete/', project_delete_view, name='project_delete'),

    path('files/<int:pk>/edit/', project_file_edit_view, name='project_file_edit'),
    path('files/<int:pk>/delete/', project_file_delete_view, name='project_file_delete'),

    path('comments/<int:pk>/edit/', project_comment_edit_view, name='project_comment_edit'),
    path('comments/<int:pk>/delete/', project_comment_delete_view, name='project_comment_delete'),
]