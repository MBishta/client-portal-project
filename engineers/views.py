from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Engineer


@login_required
def engineer_list_view(request):
    if request.user.role != 'ADMIN':
        engineers = Engineer.objects.none()
    else:
        engineers = Engineer.objects.all()

    return render(request, 'engineers/engineer_list.html', {
        'engineers': engineers
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