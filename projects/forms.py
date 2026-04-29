from django import forms

from .models import ProjectComment, ProjectFile


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['message', 'attachment']


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file', 'description', 'visible_to_client']