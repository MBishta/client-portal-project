from django.conf import settings
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        blank=True,
        null=True
    )
    client_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name
    