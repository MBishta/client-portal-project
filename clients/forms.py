from django import forms

from accounts.models import User
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'user',
            'client_name',
            'company_name',
            'phone',
            'email',
            'address',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.filter(role='CLIENT')
        self.fields['user'].required = False