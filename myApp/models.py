from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Ishan Model Start
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    website = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name

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
    applied_on = models.DateTimeField(auto_now_add=True)   #the auto_now_add field explains that when a new instance is created, the time is switched to current date time

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"