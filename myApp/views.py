# myApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, JobSearchForm
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Job

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            ssn = form.cleaned_data.get('ssn')
            password = form.cleaned_data.get('password')
            user = authenticate(username=ssn, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = LoginForm()
    return render(request, 'myApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
def contact_us_view(request):
    # Logic for handling the contact us page
    return render(request, 'myApp/contact_us.html')

def about_us_view(request):
    # Logic for handling the about us page
    return render(request, 'myApp/about_us.html')

def team_details_view(request):
    # Logic for handling the team details page
    return render(request, 'myApp/team_details.html')

def job_search(request):
    if request.method == 'GET':
        form = JobSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Job.objects.filter(title__icontains=query)
            # Add more fields to search if needed: e.g., description__icontains=query
        else:
            results = Job.objects.all()  # Display all jobs initially
    else:
        form = JobSearchForm()
        results = Job.objects.all()  # Display all jobs initially

    return render(request, 'myApp/job_search_results.html', {'form': form, 'results': results})
class JobListView(ListView):
    model = Job
    template_name = 'myApp/job_list.html'  # Template for job list view
    context_object_name = 'jobs'  # Name of the context variable in the template
    paginate_by = 10

class JobDetailView(DetailView):
    model = Job
    template_name = 'myApp/job_detail.html'  # Replace with your template name
    context_object_name = 'job'