from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from clients.models import Client
from engineers.models import Engineer
from projects.models import Project
from projects.models import ActivityLog


from .forms import (
    PortalUserCreationForm,
    PortalUserEditForm,
    PortalUserPasswordResetForm,
)
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
    search_query = request.GET.get('q')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(role__icontains=search_query)
        ).distinct()

    return render(request, 'accounts/user_list.html', {
        'users': users,
        'search_query': search_query,
    })


@login_required
def user_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PortalUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.CREATE,
                model_name='User',
                object_name=user.username,
                description=f'User created: {user.username} with role {user.role}'
            )

            if user.role == 'CLIENT':
                return redirect(f'/clients/add/?user_id={user.id}')

            elif user.role == 'ENGINEER':
                return redirect(f'/engineers/add/?user_id={user.id}')

            return redirect('accounts:user_list')

    else:
        form = PortalUserCreationForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'page_title': 'Add User',
        'button_text': 'Create User',
        'is_edit': False,
    })

@login_required
def user_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'reset_password':
            password_form = PortalUserPasswordResetForm(request.POST)

            if password_form.is_valid():
                user_obj.set_password(password_form.cleaned_data['new_password'])
                user_obj.save()
                return redirect(f'/accounts/users/{user_obj.pk}/edit/?password_changed=1')

            form = PortalUserEditForm(instance=user_obj)

        else:
            form = PortalUserEditForm(request.POST, instance=user_obj)
            password_form = PortalUserPasswordResetForm()

            if form.is_valid():
                form.save()
                return redirect('accounts:user_list')
    else:
        form = PortalUserEditForm(instance=user_obj)
        password_form = PortalUserPasswordResetForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'password_form': password_form,
        'user_obj': user_obj,
        'page_title': 'Edit User',
        'button_text': 'Save Changes',
        'is_edit': True,
        'password_changed': request.GET.get('password_changed'),
    })


@login_required
def user_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        # Prevent deleting the currently logged-in user
        if user_obj == request.user:
            return redirect('accounts:user_list')

        # Prevent deleting the last admin user
        if user_obj.role == 'ADMIN':
            admin_count = User.objects.filter(role='ADMIN').count()

            if admin_count <= 1:
                return redirect('accounts:user_list')

        user_obj.delete()

    return redirect('accounts:user_list')


@login_required
def user_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if user_obj == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('accounts:user_list')

        if user_obj.role == 'ADMIN':
            admin_count = User.objects.filter(role='ADMIN').count()

            if admin_count <= 1:
                messages.error(request, 'You cannot delete the last admin account.')
                return redirect('accounts:user_list')

        user_obj.delete()
        messages.success(request, 'User deleted successfully.')

    return redirect('accounts:user_list')


@login_required
def user_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')

        deleted_count = 0
        skipped_own_account = False
        skipped_last_admin = False

        if selected_users:
            users_to_delete = User.objects.filter(id__in=selected_users)

            for user_obj in users_to_delete:
                if user_obj == request.user:
                    skipped_own_account = True
                    continue

                if user_obj.role == 'ADMIN':
                    admin_count = User.objects.filter(role='ADMIN').count()

                    if admin_count <= 1:
                        skipped_last_admin = True
                        continue

                user_obj.delete()
                deleted_count += 1

        if deleted_count > 0:
            messages.success(request, f'{deleted_count} user(s) deleted successfully.')

        if skipped_own_account:
            messages.error(request, 'Your own account was not deleted.')

        if skipped_last_admin:
            messages.error(request, 'The last admin account was not deleted.')

    return redirect('accounts:user_list')