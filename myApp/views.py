from django.contrib.auth import logout
from django.http import HttpResponse

from .forms import JobForm, CompanyForm, JobSearchForm, ApplicationForm

from myApp.forms import ProfileForm, UserRegistrationForm
from myApp.models import Job
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Application, ApplicationReview
from .forms import ApplicationReviewForm


# Create your views here.
def home(request):

    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()  # Default queryset

    if form.is_valid():
        keywords = form.cleaned_data.get('keywords')
        location = form.cleaned_data.get('location')
        job_type = form.cleaned_data.get('job_type')

        # Filter jobs based on form inputs
        jobs = Job.objects.all()  # Initialize queryset
        if keywords:
            jobs = jobs.filter(title__icontains=keywords)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)

    context = {
        'form': form,
        'jobs': jobs,
    }
    return render(request, 'myApp/home.html', context)

def jobs(request):
    jobs_lists = Job.objects.all()
    context = {
        'title': 'Jobs Page',
        'jobs_lists': jobs_lists,
    }
    return render(request, 'myApp/jobs.html', context)

def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myApp:jobs')  # Assuming you have a view to list jobs
    else:
        form = JobForm()
    return render(request, 'job/add_job.html', {'form': form})

def addCompany(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Assuming you have a view to list jobs
    else:
        form = CompanyForm()
    return render(request, 'myApp/add_Company.html', {'form': form})

def about_us(request):
    context = {
        'title': 'About Us Page',
    }
    return render(request, 'myApp/about_us.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page upon successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'myApp/register.html', {'form': form})


# @login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('myApp:profile')  # Redirect to profile page upon successful update
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form
    }
    return render(request, 'myApp/user_profile.html', context)

# @login_required
def logout_view(request):
    logout(request)
    return redirect('myApp:home')  # Redirect to home page after logout


@login_required
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    company = job.company
    already_applied = Application.objects.filter(job=job, user=request.user).exists()

    if already_applied:
        print("User has already applied for this job.")
        return render(request, 'myApp/apply_job.html', {
            'already_applied': True,
            'job': job,
            'company': company
        })

    if request.method == 'POST':
        print("Received POST request.")
        form = ApplicationForm(request.POST, request.FILES, user=request.user, job=job, company=company)
        if form.is_valid():
            print("Form is valid.")
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.company = company
            application.status = 'P'  # Setting status to 'Pending'
            application.save()
            print("Application saved. Redirecting to job detail page.")
            return redirect('myApp:job_detail', job_id=job.id)
        else:
            print("Form is not valid.")
            print(form.errors)
    else:
        print("Received GET request.")
        form = ApplicationForm(initial={'status': 'P'}, user=request.user, job=job, company=company)

    return render(request, 'myApp/apply_job.html', {
        'form': form,
        'job': job,
        'company': company,
        'already_applied': already_applied
    })

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = Application.objects.filter(job=job, user=request.user)
    return render(request, 'Job/job_detail.html', {'job': job, 'applications': applications})


@login_required
@user_passes_test(lambda u: u.is_staff)
def update_application_review(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('myApp:manage_applications')
    else:
        form = ApplicationReviewForm(instance=application)
    return render(request, 'myApp/update_application_review.html', {'form': form, 'application': application})

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_applications(request):
    # Assuming a user can be associated with multiple companies
    companies = request.user.companies.all()  # Get all companies the user is associated with

    # For simplicity, let's assume we are only dealing with the first company
    company = companies.first()

    if not company:
        return HttpResponse("No company associated with this user.", status=403)

    applications = Application.objects.filter(company=company)
    return render(request, 'myApp/manage_applications.html', {'applications': applications})