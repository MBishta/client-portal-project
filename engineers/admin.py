from django.contrib import admin

from .models import Engineer


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('engineer_name', 'user', 'phone', 'email', 'specialization', 'is_active', 'created_at')
    list_filter = ('is_active', 'specialization', 'created_at')
    search_fields = ('engineer_name', 'user__username', 'phone', 'email', 'specialization')