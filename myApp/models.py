from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Define job type choices
JOB_TYPE = [
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Freelance', 'Freelance'),
    ('Internship', 'Internship'),
]

# Image upload function
def image_upload(instance, filename):
    return f'jobs/{instance.id}/{filename}'

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Job Model
class Job(models.Model):
    title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=15, choices=JOB_TYPE)
    description = models.TextField(max_length=1000)
    published_at = models.DateTimeField(auto_now=True)
    vacancy = models.IntegerField(default=1)
    salary = models.IntegerField(default=0)
    experience = models.IntegerField(default=1)
    image = models.ImageField(upload_to=image_upload)
    slug = models.SlugField(blank=True, null=True)

    # Relations
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwgargs)

    def __str__(self):
        return self.title
