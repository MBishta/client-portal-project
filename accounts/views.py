from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from clients.models import Client
from engineers.models import Engineer
from projects.models import Project


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@login_required
def dashboard_view(request):
    context = {}

    if request.user.role == 'ADMIN':
        context['total_clients'] = Client.objects.count()
        context['total_engineers'] = Engineer.objects.count()
        context['total_projects'] = Project.objects.count()

    elif request.user.role == 'ENGINEER':
        my_projects = Project.objects.filter(
            assigned_engineers__user=request.user
        )
        context['my_projects_count'] = my_projects.count()
        context['new_projects_count'] = my_projects.filter(status='NEW').count()
        context['in_progress_projects_count'] = my_projects.filter(status='IN_PROGRESS').count()
        context['waiting_client_projects_count'] = my_projects.filter(status='WAITING_CLIENT').count()
        context['completed_projects_count'] = my_projects.filter(status='COMPLETED').count()
        context['cancelled_projects_count'] = my_projects.filter(status='CANCELLED').count()

    elif request.user.role == 'CLIENT':
        my_projects = Project.objects.filter(
            client__user=request.user
        )
        context['my_projects_count'] = my_projects.count()
        context['active_projects_count'] = my_projects.exclude(
            status='COMPLETED'
        ).exclude(
            status='CANCELLED'
        ).count()

    return render(request, 'accounts/dashboard.html', context)