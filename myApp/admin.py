from django.contrib import admin
from .models import Company, Job, Application, Profile

# Register your models here.

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Profile)
