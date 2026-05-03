from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


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

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clients:client_list')
    else:
        form = ClientForm()

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
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
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