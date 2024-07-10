from django.contrib import admin
from .models import Job, Company

admin.site.register(Company)
admin.site.register(Job)