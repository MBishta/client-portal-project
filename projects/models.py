from django.db import models

from clients.models import Client
from engineers.models import Engineer


class Project(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WAITING_CLIENT = 'WAITING_CLIENT', 'Waiting Client'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class Stage(models.TextChoices):
        PROJECT_REGISTERED = 'PROJECT_REGISTERED', 'Project Registered'
        REQUIREMENTS_COLLECTED = 'REQUIREMENTS_COLLECTED', 'Requirements Collected'
        SITE_VISIT = 'SITE_VISIT', 'Site Visit'
        CONCEPT_DESIGN = 'CONCEPT_DESIGN', 'Concept Design'
        CLIENT_REVIEW = 'CLIENT_REVIEW', 'Client Review'
        REVISIONS = 'REVISIONS', 'Revisions'
        FINAL_DESIGN = 'FINAL_DESIGN', 'Final Design'
        DRAWINGS_PREPARATION = 'DRAWINGS_PREPARATION', 'Drawings Preparation'
        MUNICIPALITY_SUBMISSION = 'MUNICIPALITY_SUBMISSION', 'Municipality Submission'
        APPROVAL_STAGE = 'APPROVAL_STAGE', 'Approval Stage'
        SUPERVISION_EXECUTION = 'SUPERVISION_EXECUTION', 'Supervision / Execution'
        COMPLETED = 'COMPLETED', 'Completed'

    project_name = models.CharField(max_length=200)
    project_code = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    assigned_engineers = models.ManyToManyField(
    Engineer,
    blank=True,
    related_name='projects'
     ) 
    project_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    current_stage = models.CharField(
        max_length=50,
        choices=Stage.choices,
        default=Stage.PROJECT_REGISTERED
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_code} - {self.project_name}"


class ProjectFile(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=200, blank=True, null=True)
    visible_to_client = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_code} - {self.description or self.file.name}"
    

class ProjectComment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='project_comments'
    )
    message = models.TextField()
    attachment = models.FileField(upload_to='project_comments/', blank=True, null=True)
    visible_to_client = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_code} - {self.sender.username}"