from django.contrib import admin

from .models import Project, ProjectFile, ProjectComment


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    fields = ('file', 'description', 'visible_to_client')
    readonly_fields = ('uploaded_at',)


class ProjectCommentInline(admin.TabularInline):
    model = ProjectComment
    extra = 1
    fields = ('sender', 'message', 'attachment', 'visible_to_client')
    readonly_fields = ('created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_code',
        'project_name',
        'client',
        'assigned_engineer',
        'current_stage',
        'status',
        'created_at',
    )
    list_filter = ('status', 'current_stage', 'project_type', 'created_at')
    search_fields = (
        'project_code',
        'project_name',
        'client__client_name',
        'assigned_engineer__engineer_name',
    )
    inlines = [ProjectFileInline, ProjectCommentInline]


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'description',
        'visible_to_client',
        'uploaded_at',
    )
    list_filter = ('visible_to_client', 'uploaded_at')
    search_fields = (
        'project__project_code',
        'project__project_name',
        'description',
    )


@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'sender',
        'visible_to_client',
        'created_at',
    )
    list_filter = ('visible_to_client', 'created_at')
    search_fields = (
        'project__project_code',
        'project__project_name',
        'sender__username',
        'message',
    )