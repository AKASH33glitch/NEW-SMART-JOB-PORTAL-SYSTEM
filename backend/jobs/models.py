from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    posted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
