from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from clients.models import Client
from engineers.models import Engineer
from projects.models import Project

from .forms import PortalUserCreationForm, PortalUserEditForm
from .models import User


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@login_required
def dashboard_view(request):
    context = {}

    if request.user.role == 'ADMIN':
        context['total_users'] = User.objects.count()
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


@login_required
def user_list_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    users = User.objects.all()

    return render(request, 'accounts/user_list.html', {
        'users': users
    })


@login_required
def user_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PortalUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
    else:
        form = PortalUserCreationForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'page_title': 'Add User',
        'button_text': 'Create User',
    })


@login_required
def user_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = PortalUserEditForm(request.POST, instance=user_obj)

        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
    else:
        form = PortalUserEditForm(instance=user_obj)

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'page_title': 'Edit User',
        'button_text': 'Save Changes',
    })


@login_required
def user_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user_obj.delete()

    return redirect('accounts:user_list')


@login_required
def user_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')

        if selected_users:
            User.objects.filter(id__in=selected_users).delete()

    return redirect('accounts:user_list')