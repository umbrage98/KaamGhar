from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    JOB_TYPES = [
        ('fulltime', 'Full-Time'),
        ('parttime', 'Part-Time'),
        ('intern', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100)
    vacancies = models.PositiveIntegerField()
    deadline = models.DateField()
    description = models.TextField()
    requirements = models.TextField(blank=True)

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
