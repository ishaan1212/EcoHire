from django.contrib import admin
from .models import Company, Job, Application, Profile


# Customizing Company model admin
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'website')
    search_fields = ('name', 'location')
    list_filter = ('location',)


# Customizing Job model admin
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'salary', 'published_at')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('job_type', 'currency', 'published_at')
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)


# Customizing Application model admin
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'company', 'status', 'applied_on')
    search_fields = ('user__username', 'job__title', 'company__name')
    list_filter = ('status', 'applied_on')
    ordering = ('-applied_on',)


# Customizing Profile model admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'country')
    search_fields = ('user__username', 'city', 'country')
    list_filter = ('city', 'country')


# Registering models with admin site
admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Profile, ProfileAdmin)

