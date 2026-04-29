from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Project


@login_required
def project_list_view(request):
    if request.user.role == 'ADMIN':
        projects = Project.objects.all()

    elif request.user.role == 'ENGINEER':
        projects = Project.objects.filter(
            assigned_engineer__user=request.user
        )

    else:
        projects = Project.objects.none()

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })
