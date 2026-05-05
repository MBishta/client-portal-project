from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client
from projects.models import ActivityLog


@login_required
def client_list_view(request):
    if request.user.role != 'ADMIN':
        clients = Client.objects.none()
    else:
        clients = Client.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        clients = clients.filter(
        Q(client_name__icontains=search_query) |
        Q(company_name__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(user__username__icontains=search_query)
    ).distinct()
    
    return render(request, 'clients/client_list.html', {
    'clients': clients,
    'search_query': search_query,
})


@login_required
def client_detail_view(request, pk):
    if request.user.role != 'ADMIN':
        client = None
        projects = []
    else:
        client = get_object_or_404(Client, pk=pk)
        projects = client.projects.all()

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'projects': projects,
    })

@login_required
def client_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    user_id = request.GET.get('user_id')

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.CREATE,
                model_name='Client',
                object_name=str(client),
                description=f'Client created: {client.client_name}'
            )

            return redirect('clients:client_list')
    else:
        initial_data = {}

        if user_id:
            initial_data['user'] = user_id

        form = ClientForm(initial=initial_data)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'page_title': 'Add Client',
        'button_text': 'Save Client',
    })


@login_required
def client_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        old_user = client.user
        old_client_name = client.client_name
        old_company_name = client.company_name
        old_phone = client.phone
        old_email = client.email
        old_address = client.address
        old_is_active = client.is_active

        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            client = form.save()

            changes = []

            if old_user != client.user:
                changes.append(f'User: {old_user} -> {client.user}')

            if old_client_name != client.client_name:
                changes.append(f'Client Name: {old_client_name} -> {client.client_name}')

            if old_company_name != client.company_name:
                changes.append(f'Company Name: {old_company_name} -> {client.company_name}')

            if old_phone != client.phone:
                changes.append(f'Phone: {old_phone} -> {client.phone}')

            if old_email != client.email:
                changes.append(f'Email: {old_email} -> {client.email}')

            if old_address != client.address:
                changes.append('Address changed')

            if old_is_active != client.is_active:
                changes.append(f'Active: {old_is_active} -> {client.is_active}')

            description = f'Client updated: {client.client_name}'

            if changes:
                description += ' | Changes: ' + ', '.join(changes)

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.UPDATE,
                model_name='Client',
                object_name=str(client),
                description=description
            )

            return redirect('clients:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'page_title': 'Edit Client',
        'button_text': 'Save Changes',
    })

@login_required
def client_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()
        return redirect('clients:client_list')

    return redirect('clients:client_detail', pk=client.pk)


@login_required
def client_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_clients = request.POST.getlist('selected_clients')

        if selected_clients:
            Client.objects.filter(id__in=selected_clients).delete()

    return redirect('clients:client_list')