import re

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

        labels = {
            'user': 'User Account *',
            'client_name': 'Client Name *',
            'company_name': 'Company Name',
            'phone': 'Mobile Number *',
            'email': 'Email *',
            'address': 'Address',
            'is_active': 'Active',
        }

        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Numbers only',
                'inputmode': 'numeric',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.filter(role='CLIENT')
        self.fields['user'].required = True
        self.fields['client_name'].required = True
        self.fields['phone'].required = True
        self.fields['email'].required = True

    def clean_client_name(self):
        client_name = self.cleaned_data.get('client_name')

        if client_name and not re.match(r'^[A-Za-z\s]+$', client_name):
            raise forms.ValidationError('Client name should contain letters and spaces only.')

        return client_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and not phone.isdigit():
            raise forms.ValidationError('Mobile number should contain numbers only.')

        return phone