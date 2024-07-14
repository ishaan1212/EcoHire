from django.contrib import admin
from .models import Job, Company, Application, Profile

# Register your models here.

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Profile)

