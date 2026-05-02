from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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