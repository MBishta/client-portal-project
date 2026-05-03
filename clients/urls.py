from django.urls import path

from .views import (
    client_list_view,
    client_detail_view,
    client_create_view,
    client_edit_view,
    client_delete_view,
)

app_name = 'clients'

urlpatterns = [
    path('', client_list_view, name='client_list'),
    path('add/', client_create_view, name='client_add'),
    path('<int:pk>/', client_detail_view, name='client_detail'),
    path('<int:pk>/edit/', client_edit_view, name='client_edit'),
    path('<int:pk>/delete/', client_delete_view, name='client_delete'),
]