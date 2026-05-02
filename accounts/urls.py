from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, dashboard_view, user_create_view

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('users/add/', user_create_view, name='user_add'),
]