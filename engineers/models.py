from django.conf import settings
from django.db import models


class Engineer(models.Model):
    class Department(models.TextChoices):
        INTERIOR_DESIGNER = 'INTERIOR_DESIGNER', 'Interior Designer'
        MECHANICAL_ENGINEER = 'MECHANICAL_ENGINEER', 'Mechanical Engineer'
        ELECTRICAL_ENGINEER = 'ELECTRICAL_ENGINEER', 'Electrical Engineer'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor'
        ARCHITECT = 'ARCHITECT', 'Architect'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='engineer_profile'
    )
    engineer_name = models.CharField(max_length=150)
    department = models.CharField(
        max_length=50,
        choices=Department.choices,
        blank=True,
        null=True
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    specialization = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.engineer_name