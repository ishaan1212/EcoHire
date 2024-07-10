from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    location = models.CharField(max_length=50)
    website = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, default='CA')

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
