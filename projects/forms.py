from django import forms

from .models import Project, ProjectComment, ProjectFile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name',
            'project_code',
            'client',
            'assigned_engineers',
            'project_type',
            'location',
            'start_date',
            'expected_end_date',
            'current_stage',
            'status',
            'description',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_end_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_engineers': forms.SelectMultiple(attrs={'size': 6}),
        }


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['message', 'attachment']


class ProjectCommentEditForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['message', 'attachment', 'visible_to_client']


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file', 'description', 'visible_to_client']