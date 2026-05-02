from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def client_list_view(request):
    if request.user.role != 'ADMIN':
        clients = Client.objects.none()
    else:
        clients = Client.objects.all()

    return render(request, 'clients/client_list.html', {
        'clients': clients
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
        'form': form
    })