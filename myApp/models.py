from datetime import timezone
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='companies')  # Assuming many-to-many relationship
    is_eco_verified = models.BooleanField(default=False)
    eco_verified_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Freelance', 'Freelance'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('CAD', 'CAD'),
        ('INR', 'INR')
        # Add more currencies as needed
    ]
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full Time')
    location = models.CharField(max_length=50)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    published_at = models.DateTimeField(auto_now_add=True)

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
    applied_on = models.DateTimeField(
        auto_now_add=True)  #the auto_now_add field explains that when a new instance is created, the time is switched to current date time
    motivation_letter = models.TextField(default='')  # New field for motivation letter
    experience = models.TextField(default='')  # New field for experience related to environment
    skills = models.TextField(default='')  # New field for skills related to environment

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_recruiter = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ApplicationReview(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='P')
    comments = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.user.username} - {self.application.job.title} - {self.get_status_display()}"


class EnvironmentalInitiative(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class UserContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initiative = models.ForeignKey(EnvironmentalInitiative, on_delete=models.CASCADE)
    contribution_details = models.TextField()
    contribution_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.initiative.title}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class EcoSurvey(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True)

    energy_efficiency = models.IntegerField(default=0)
    waste_management = models.IntegerField(default=0)
    sustainable_sourcing = models.IntegerField(default=0)
    water_conservation = models.IntegerField(default=0)
    employee_training = models.IntegerField(default=0)
    green_certifications = models.IntegerField(default=0)
    carbon_footprint = models.IntegerField(default=0)
    renewable_energy = models.IntegerField(default=0)

    @property
    def total_score(self):
        return (
                self.energy_efficiency +
                self.waste_management +
                self.sustainable_sourcing +
                self.water_conservation +
                self.employee_training +
                self.green_certifications +
                self.carbon_footprint +
                self.renewable_energy
        )


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}'
