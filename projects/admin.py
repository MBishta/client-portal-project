from django.contrib import admin

from .models import Project


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
    search_fields = ('project_code', 'project_name', 'client__client_name', 'assigned_engineer__engineer_name')