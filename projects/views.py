from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Project


@login_required
def project_list_view(request):
    if request.user.role == 'ADMIN':
        projects = Project.objects.all()

    elif request.user.role == 'ENGINEER':
        projects = Project.objects.filter(
            assigned_engineer__user=request.user
        )

    elif request.user.role == 'CLIENT':
        projects = Project.objects.filter(
            client__user=request.user
        )

    else:
        projects = Project.objects.none()

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })


@login_required
def project_detail_view(request, pk):
    if request.user.role == 'ADMIN':
        project = get_object_or_404(Project, pk=pk)

    elif request.user.role == 'ENGINEER':
        project = get_object_or_404(
            Project,
            pk=pk,
            assigned_engineer__user=request.user
        )

    elif request.user.role == 'CLIENT':
        project = get_object_or_404(
            Project,
            pk=pk,
            client__user=request.user
        )

    else:
        project = None

    return render(request, 'projects/project_detail.html', {
        'project': project
    })