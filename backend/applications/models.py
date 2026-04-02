from django.db import models

class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    applicant = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    cover_letter = models.TextField(blank=True)
    cv = models.FileField(upload_to='applications/', blank=True, null=True)  # If different from profile CV
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"
