from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ProjectForm,
    ProjectCommentForm,
    ProjectCommentEditForm,
    ProjectFileForm,
)
from .models import ActivityLog, Project, ProjectComment, ProjectFile


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

    if status_filter:
        projects = projects.filter(status=status_filter)

    if search_query:
        projects = projects.filter(
            Q(project_name__icontains=search_query) |
            Q(project_code__icontains=search_query) |
            Q(client__client_name__icontains=search_query) |
            Q(assigned_engineers__engineer_name__icontains=search_query)
        ).distinct()

    paginator = Paginator(projects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'page_obj': page_obj,
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
            project = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.CREATE,
                model_name='Project',
                object_name=str(project),
                description=f'Project created: {project.project_name}'
            )

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
        old_project_name = project.project_name
        old_project_code = project.project_code
        old_client = project.client
        old_project_type = project.project_type
        old_location = project.location
        old_start_date = project.start_date
        old_expected_end_date = project.expected_end_date
        old_current_stage = project.current_stage
        old_status = project.status
        old_description = project.description

        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()

            changes = []

            if old_project_name != project.project_name:
                changes.append(f'Project Name: {old_project_name} -> {project.project_name}')

            if old_project_code != project.project_code:
                changes.append(f'Project Code: {old_project_code} -> {project.project_code}')

            if old_client != project.client:
                changes.append(f'Client: {old_client} -> {project.client}')

            if old_project_type != project.project_type:
                changes.append(f'Project Type: {old_project_type} -> {project.project_type}')

            if old_location != project.location:
                changes.append(f'Location: {old_location} -> {project.location}')

            if old_start_date != project.start_date:
                changes.append(f'Start Date: {old_start_date} -> {project.start_date}')

            if old_expected_end_date != project.expected_end_date:
                changes.append(f'Expected End Date: {old_expected_end_date} -> {project.expected_end_date}')

            if old_current_stage != project.current_stage:
                changes.append(f'Stage: {old_current_stage} -> {project.current_stage}')

            if old_status != project.status:
                changes.append(f'Status: {old_status} -> {project.status}')

            if old_description != project.description:
                changes.append('Description changed')

            description = f'Project updated: {project.project_name}'

            if changes:
                description += ' | Changes: ' + ', '.join(changes)

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.UPDATE,
                model_name='Project',
                object_name=str(project),
                description=description
            )

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
        project_name = str(project)

        ActivityLog.objects.create(
            user=request.user,
            action=ActivityLog.Action.DELETE,
            model_name='Project',
            object_name=project_name,
            description=f'Project deleted: {project_name}'
        )

        project.delete()
        return redirect('projects:project_list')

    return redirect('projects:project_detail', pk=project.pk)


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

                ActivityLog.objects.create(
                    user=request.user,
                    action=ActivityLog.Action.CREATE,
                    model_name='ProjectComment',
                    object_name=f'Comment on {project}',
                    description=f'Comment added on project: {project}'
                )

                return redirect('projects:project_detail', pk=project.pk)

        elif form_type == 'file' and request.user.role in ['ADMIN', 'ENGINEER']:
            file_form = ProjectFileForm(request.POST, request.FILES)

            if file_form.is_valid():
                project_file = file_form.save(commit=False)
                project_file.project = project
                project_file.uploaded_by = request.user
                project_file.save()

                ActivityLog.objects.create(
                    user=request.user,
                    action=ActivityLog.Action.CREATE,
                    model_name='ProjectFile',
                    object_name=project_file.file.name,
                    description=f'File uploaded to project: {project}'
                )

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
    old_description = project_file.description
    old_visible_to_client = project_file.visible_to_client
    old_file_name = project_file.file.name

    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES, instance=project_file)

        if form.is_valid():
            project_file = form.save()

            changes = []

            if old_description != project_file.description:
                changes.append('Description changed')

            if old_visible_to_client != project_file.visible_to_client:
                changes.append(f'Visible to Client: {old_visible_to_client} -> {project_file.visible_to_client}')

            if old_file_name != project_file.file.name:
                changes.append(f'File changed: {old_file_name} -> {project_file.file.name}')

            description = f'File updated on project: {project_file.project}'

            if changes:
                description += ' | Changes: ' + ', '.join(changes)

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.UPDATE,
                model_name='ProjectFile',
                object_name=project_file.file.name,
                description=description
            )

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
    project_name = str(project_file.project)
    file_name = project_file.file.name

    if request.method == 'POST':
        ActivityLog.objects.create(
            user=request.user,
            action=ActivityLog.Action.DELETE,
            model_name='ProjectFile',
            object_name=file_name,
            description=f'File deleted from project: {project_name}'
        )

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
    old_message = comment.message
    old_attachment = comment.attachment.name if comment.attachment else ''
    old_visible_to_client = comment.visible_to_client

    if request.method == 'POST':
        form = ProjectCommentEditForm(request.POST, request.FILES, instance=comment)

        if form.is_valid():
            comment = form.save()

            changes = []

            if old_message != comment.message:
                changes.append('Message changed')

            new_attachment = comment.attachment.name if comment.attachment else ''

            if old_attachment != new_attachment:
                changes.append(f'Attachment changed: {old_attachment or "None"} -> {new_attachment or "None"}')

            if old_visible_to_client != comment.visible_to_client:
                changes.append(f'Visible to Client: {old_visible_to_client} -> {comment.visible_to_client}')

            description = f'Comment updated on project: {comment.project}'

            if changes:
                description += ' | Changes: ' + ', '.join(changes)

            ActivityLog.objects.create(
                user=request.user,
                action=ActivityLog.Action.UPDATE,
                model_name='ProjectComment',
                object_name=f'Comment on {comment.project}',
                description=description
            )

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
    project_name = str(comment.project)

    if request.method == 'POST':
        ActivityLog.objects.create(
            user=request.user,
            action=ActivityLog.Action.DELETE,
            model_name='ProjectComment',
            object_name=f'Comment on {project_name}',
            description=f'Comment deleted from project: {project_name}'
        )

        comment.delete()

    return redirect('projects:project_detail', pk=project_pk)


@login_required
def project_bulk_delete_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        selected_projects = request.POST.getlist('selected_projects')

        if selected_projects:
            projects_to_delete = Project.objects.filter(id__in=selected_projects)

            for project in projects_to_delete:
                project_name = str(project)

                ActivityLog.objects.create(
                    user=request.user,
                    action=ActivityLog.Action.DELETE,
                    model_name='Project',
                    object_name=project_name,
                    description=f'Project deleted: {project_name}'
                )

                project.delete()

    return redirect('projects:project_list')