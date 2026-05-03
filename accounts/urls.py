from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CustomLoginView,
    dashboard_view,
    user_list_view,
    user_create_view,
    user_edit_view,
    user_delete_view,
    user_bulk_delete_view,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('users/', user_list_view, name='user_list'),
    path('users/add/', user_create_view, name='user_add'),
    path('users/bulk-delete/', user_bulk_delete_view, name='user_bulk_delete'),
    path('users/<int:pk>/edit/', user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', user_delete_view, name='user_delete'),
]