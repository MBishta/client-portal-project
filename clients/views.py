from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

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