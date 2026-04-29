from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectCommentForm
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
        files = project.files.all()
        comments = project.comments.all()

    elif request.user.role == 'ENGINEER':
        project = get_object_or_404(
            Project,
            pk=pk,
            assigned_engineer__user=request.user
        )
        files = project.files.all()
        comments = project.comments.all()

    elif request.user.role == 'CLIENT':
        project = get_object_or_404(
            Project,
            pk=pk,
            client__user=request.user
        )
        files = project.files.filter(visible_to_client=True)
        comments = project.comments.filter(visible_to_client=True)

    else:
        project = None
        files = []
        comments = []

    if request.method == 'POST' and project:
        form = ProjectCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.sender = request.user

            if request.user.role == 'CLIENT':
                comment.visible_to_client = True

            comment.save()
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectCommentForm()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'files': files,
        'comments': comments,
        'form': form,
    })