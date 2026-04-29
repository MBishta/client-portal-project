from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'client_name',
        'user',
        'company_name',
        'phone',
        'email',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'created_at')
    search_fields = (
        'client_name',
        'user__username',
        'company_name',
        'phone',
        'email',
    )