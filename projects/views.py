from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ProjectForm,
    ProjectCommentForm,
    ProjectCommentEditForm,
    ProjectFileForm,
)
from .models import Project, ProjectComment, ProjectFile


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


    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    if status_filter: projects = projects.filter(status=status_filter)

    if search_query: projects = projects.filter(
        Q(project_name__icontains=search_query) |
        Q(project_code__icontains=search_query) |
        Q(client__client_name__icontains=search_query) |
        Q(assigned_engineers__engineer_name__icontains=search_query)
    ).distinct()
        
    return render(request, 'projects/project_list.html', {

    'projects': projects,
    'status_filter': status_filter,
    'search_query': search_query,
})


@login_required
def project_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('projects:project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'page_title': 'Add Project',
        'button_text': 'Save Project',
    })


@login_required
def project_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': form,
        'page_title': 'Edit Project',
        'button_text': 'Save Changes',
    })


@login_required
def project_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects:project_list')

    return render(request, 'projects/project_confirm_delete.html', {
        'project': project
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
                project_file.uploaded_by = request.user
                project_file.save()
                return redirect('projects:project_detail', pk=project.pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'files': files,
        'comments': comments,
        'comment_form': comment_form,
        'file_form': file_form,
    })


@login_required
def project_file_edit_view(request, pk):
    project_file = get_object_or_404(
        ProjectFile,
        pk=pk,
        uploaded_by=request.user
    )

    project_pk = project_file.project.pk

    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES, instance=project_file)

        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', pk=project_pk)
    else:
        form = ProjectFileForm(instance=project_file)

    return render(request, 'projects/project_file_edit.html', {
        'form': form,
        'project_file': project_file,
    })


@login_required
def project_file_delete_view(request, pk):
    project_file = get_object_or_404(
        ProjectFile,
        pk=pk,
        uploaded_by=request.user
    )

    project_pk = project_file.project.pk

    if request.method == 'POST':
        project_file.delete()

    return redirect('projects:project_detail', pk=project_pk)


@login_required
def project_comment_edit_view(request, pk):
    comment = get_object_or_404(
        ProjectComment,
        pk=pk,
        sender=request.user
    )

    project_pk = comment.project.pk

    if request.method == 'POST':
        form = ProjectCommentEditForm(request.POST, request.FILES, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', pk=project_pk)
    else:
        form = ProjectCommentEditForm(instance=comment)

    return render(request, 'projects/project_comment_edit.html', {
        'form': form,
        'comment': comment,
    })


@login_required
def project_comment_delete_view(request, pk):
    comment = get_object_or_404(
        ProjectComment,
        pk=pk,
        sender=request.user
    )

    project_pk = comment.project.pk

    if request.method == 'POST':
        comment.delete()

    return redirect('projects:project_detail', pk=project_pk)

@login_required
def project_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_projects = request.POST.getlist('selected_projects')

        if selected_projects:
            Project.objects.filter(id__in=selected_projects).delete()

    return redirect('projects:project_list')