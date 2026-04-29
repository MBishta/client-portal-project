from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectCommentForm, ProjectFileForm
from .models import Project


@login_required
def project_list_view(request):
    if request.user.role == 'ADMIN':
        projects = Project.objects.all()

    elif request.user.role == 'ENGINEER':
        projects = Project.objects.filter(
            assigned_engineers__user=request.user
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
            assigned_engineers__user=request.user
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

    comment_form = ProjectCommentForm()
    file_form = ProjectFileForm()

    if request.method == 'POST' and project:
        form_type = request.POST.get('form_type')

        if form_type == 'comment':
            comment_form = ProjectCommentForm(request.POST, request.FILES)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.sender = request.user

                if request.user.role == 'CLIENT':
                    comment.visible_to_client = True

                comment.save()
                return redirect('projects:project_detail', pk=project.pk)

        elif form_type == 'file' and request.user.role in ['ADMIN', 'ENGINEER']:
            file_form = ProjectFileForm(request.POST, request.FILES)

            if file_form.is_valid():
                project_file = file_form.save(commit=False)
                project_file.project = project
                project_file.save()
                return redirect('projects:project_detail', pk=project.pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'files': files,
        'comments': comments,
        'comment_form': comment_form,
        'file_form': file_form,
    })