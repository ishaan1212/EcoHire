from django.views.generic import ListView, DetailView
from .models import Job

class IndexView(ListView):
    model = Job
    template_name = 'Job/index.html'
    context_object_name = 'jobs'

class JobDetailView(DetailView):
    model = Job
    template_name = 'Job/job_detail.html'
    context_object_name = 'job'
