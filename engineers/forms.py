import re

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

        labels = {
            'user': 'User Account *',
            'engineer_name': 'Engineer Name *',
            'department': 'Department *',
            'phone': 'Mobile Number *',
            'email': 'Email ',
            'specialization': 'Specialization',
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

        self.fields['user'].queryset = User.objects.filter(role='ENGINEER')
        self.fields['user'].required = True
        self.fields['engineer_name'].required = True
        self.fields['department'].required = True
        self.fields['phone'].required = True
        self.fields['email'].required = False

    def clean_engineer_name(self):
        engineer_name = self.cleaned_data.get('engineer_name')

        if engineer_name and not re.match(r'^[A-Za-z\s]+$', engineer_name):
            raise forms.ValidationError('Engineer name should contain letters and spaces only.')

        return engineer_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and not phone.isdigit():
            raise forms.ValidationError('Mobile number should contain numbers only.')

        return phone