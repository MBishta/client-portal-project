from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EngineerForm
from .models import Engineer
from projects.models import ActivityLog


@login_required
def engineer_list_view(request):
    if request.user.role != 'ADMIN':
        engineers = Engineer.objects.none()
    else:
        engineers = Engineer.objects.all()

    search_query = request.GET.get('q')

    if search_query:
        engineers = engineers.filter(
            Q(engineer_name__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).distinct()

    return render(request, 'engineers/engineer_list.html', {
        'engineers': engineers,
        'search_query': search_query,
    })


@login_required
def engineer_detail_view(request, pk):
    if request.user.role != 'ADMIN':
        engineer = None
        projects = []
    else:
        engineer = get_object_or_404(Engineer, pk=pk)
        projects = engineer.projects.all()

    return render(request, 'engineers/engineer_detail.html', {
        'engineer': engineer,
        'projects': projects,
    })


@login_required
def engineer_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_id = request.GET.get('user_id')

    if request.method == 'POST':
        form = EngineerForm(request.POST)

        if form.is_valid():
            engineer = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.CREATE,
                model_name='Engineer',
                object_name=str(engineer),
                description=f'Engineer created: {engineer.engineer_name}'
            )

            return redirect('engineers:engineer_list')
    else:
        initial_data = {}

        if user_id:
            initial_data['user'] = user_id

        form = EngineerForm(initial=initial_data)

    return render(request, 'engineers/engineer_form.html', {
        'form': form,
        'page_title': 'Add Engineer',
        'button_text': 'Save Engineer',
    })


@login_required
def engineer_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    engineer = get_object_or_404(Engineer, pk=pk)

    if request.method == 'POST':
        old_user = engineer.user
        old_engineer_name = engineer.engineer_name
        old_department = engineer.department
        old_phone = engineer.phone
        old_email = engineer.email
        old_specialization = engineer.specialization
        old_is_active = engineer.is_active

        form = EngineerForm(request.POST, instance=engineer)

        if form.is_valid():
            engineer = form.save()

            changes = []

            if old_user != engineer.user:
                changes.append(f'User: {old_user} -> {engineer.user}')

            if old_engineer_name != engineer.engineer_name:
                changes.append(f'Engineer Name: {old_engineer_name} -> {engineer.engineer_name}')

            if old_department != engineer.department:
                changes.append(f'Department: {old_department} -> {engineer.department}')

            if old_phone != engineer.phone:
                changes.append(f'Phone: {old_phone} -> {engineer.phone}')

            if old_email != engineer.email:
                changes.append(f'Email: {old_email} -> {engineer.email}')

            if old_specialization != engineer.specialization:
                changes.append(f'Specialization: {old_specialization} -> {engineer.specialization}')

            if old_is_active != engineer.is_active:
                changes.append(f'Active: {old_is_active} -> {engineer.is_active}')

            description = f'Engineer updated: {engineer.engineer_name}'

            if changes:
                description += ' | Changes: ' + ', '.join(changes)

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.UPDATE,
                model_name='Engineer',
                object_name=str(engineer),
                description=description
            )

            return redirect('engineers:engineer_detail', pk=engineer.pk)
    else:
        form = EngineerForm(instance=engineer)

    return render(request, 'engineers/engineer_form.html', {
        'form': form,
        'page_title': 'Edit Engineer',
        'button_text': 'Save Changes',
    })


@login_required
def engineer_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    engineer = get_object_or_404(Engineer, pk=pk)

    if request.method == 'POST':
        engineer_name = str(engineer)

        ActivityLog.objects.create(
            user=request.user,
            action=ActivityLog.Action.DELETE,
            model_name='Engineer',
            object_name=engineer_name,
            description=f'Engineer deleted: {engineer_name}'
        )

        engineer.delete()
        return redirect('engineers:engineer_list')

    return redirect('engineers:engineer_detail', pk=engineer.pk)

@login_required
def engineer_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_engineers = request.POST.getlist('selected_engineers')

        if selected_engineers:
            Engineer.objects.filter(id__in=selected_engineers).delete()

    return redirect('engineers:engineer_list')