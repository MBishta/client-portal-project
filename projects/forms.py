from django import forms

from .models import ProjectComment


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['message', 'attachment']