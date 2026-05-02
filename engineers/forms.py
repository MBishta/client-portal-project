from django import forms

from accounts.models import User
from .models import Engineer


class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = [
            'user',
            'engineer_name',
            'department',
            'phone',
            'email',
            'specialization',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.filter(role='ENGINEER')