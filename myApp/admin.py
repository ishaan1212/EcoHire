from django.contrib import admin
from .models import Job, Company, Profile

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Profile)
