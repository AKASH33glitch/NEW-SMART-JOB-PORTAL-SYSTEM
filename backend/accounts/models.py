from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # Common fields
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    # Job Seeker fields
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    skills = models.TextField(blank=True)  # JSON or comma separated
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True)
    # Employer fields
    company_name = models.CharField(max_length=100, blank=True)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
