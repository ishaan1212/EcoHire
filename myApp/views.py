from datetime import datetime

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.timezone import now

from .forms import JobForm, CompanyForm, JobSearchForm, ApplicationForm, EnvironmentalInitiativeForm
from myApp.models import Job, Application, Profile, Company, EnvironmentalInitiative, UserContribution
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import SignUpForm

from myApp.forms import ProfileForm, UserRegistrationForm
from myApp.models import Job
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Application, ApplicationReview
from .forms import ApplicationReviewForm
import os
from django.conf import settings


# Create your views here.
def home(request):

    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()  # Default queryset
    jobs_count = Job.objects.count()
    members_count = Profile.objects.count()
    companies_count = Company.objects.count()

    # Path to the resumes directory
    resumes_path = os.path.join(settings.MEDIA_ROOT, 'resumes')
    try:
        # List files in the directory and count them
        resumes_count = len(
            [name for name in os.listdir(resumes_path) if os.path.isfile(os.path.join(resumes_path, name))])
    except FileNotFoundError:
        resumes_count = 0

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

        # Check if 'last_login' exists in the session
    if 'last_login' in request.session:
        last_login = request.session['last_login']
        last_login_message = f"Your last login was on {last_login}"
    else:
        last_login_message = "Your last login was more than one hour ago"

    context = {
        'form': form,
        'jobs': jobs,
        'last_login_message': last_login_message,
        'jobs_count': jobs_count,
        'member_count': members_count,
        'companies_count': companies_count,
        'resumes_count': resumes_count
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
            return redirect('myApp:job_list')  # Assuming you have a view to list jobs
    else:
        form = CompanyForm()
    return render(request, 'myApp/add_Company.html', {'form': form})

def about_us(request):
    context = {
        'title': 'About Us Page',
    }
    return render(request, 'myApp/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.is_recruiter = form.cleaned_data.get('is_recruiter')
            user.save()
            login(request, user)
            if form.cleaned_data.get('is_recruiter'):
                messages.success(request, 'Signup successful! You have been logged in as a recruiter.')
                redirect_url = reverse('myApp:home')
            else:
                messages.success(request, 'Signup successful! You have been logged in as a job seeker.')
                redirect_url = reverse('myApp:home')
            return JsonResponse({'success': True, 'message': 'Signup successful! You have been logged in.', 'redirect_url': redirect_url})
        else:
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = SignUpForm()
    return render(request, 'myApp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Get the current datetime
            current_time = datetime.now()

            # Format the datetime as a string in the desired format
            formatted_time = current_time.strftime('%Y-%m-%d, %H:%M:%S')
            request.session['last_login'] = formatted_time
            request.session.set_expiry(3600)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if user.profile.is_recruiter:
                    message = 'Login successful! You have been logged in as a recruiter.'
                    redirect_url = reverse('myApp:home')  # Redirect to home
                else:
                    message = 'Login successful! You have been logged in as a job seeker.'
                    redirect_url = reverse('myApp:home')  # Redirect to home
                return JsonResponse({'success': True, 'message': message, 'redirect_url': redirect_url})
            else:
                return redirect('myApp:home')  # Redirect to home after login
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid credentials.'})
            else:
                return render(request, 'myApp/login.html', {'error_message': 'Invalid credentials.'})
    else:
        return render(request, 'myApp/login.html')
# @login_required
def logout_view(request):
    logout(request)
    return redirect('myApp:home')  # Redirect to home page after logout


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
    return render(request, 'job/job_detail.html', {'job': job, 'applications': applications})


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
def manage_applications(request):
    # Get all job applications
    applications = Application.objects.all()

    return render(request, 'myApp/manage_applications.html', {'applications': applications})


@login_required  # Ensures that only logged-in users can access this view
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('myApp:profile')  # Redirect to profile page upon successful update
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    # Fetch the applications related to the logged-in user
    applications = Application.objects.filter(user=request.user).order_by('-applied_on')

    context = {
        'profile_form': profile_form,
        'applications': applications
    }
    return render(request, 'myApp/user_profile.html', context)


@login_required
def initiatives_list(request):
    initiatives = EnvironmentalInitiative.objects.all()
    user_contributions = UserContribution.objects.filter(user=request.user)
    enrolled_initiatives_ids = user_contributions.values_list('initiative_id', flat=True)
    contributions_dict = {contribution.initiative_id: contribution for contribution in user_contributions}

    for initiative in initiatives:
        initiative.is_enrolled = initiative.id in enrolled_initiatives_ids
        initiative.contribution_id = contributions_dict[initiative.id].id if initiative.is_enrolled else None

    return render(request, 'myApp/initiatives_list.html', {'initiatives': initiatives})


@login_required
def user_contributions(request):
    contributions = UserContribution.objects.filter(user=request.user)
    return render(request, 'myApp/user_contributions.html', {'contributions': contributions})

@login_required
def enroll_initiative(request, initiative_id):
    if request.method == 'POST':
        initiative = EnvironmentalInitiative.objects.get(id=initiative_id)
        # Check if the user has already enrolled
        if not UserContribution.objects.filter(user=request.user, initiative=initiative).exists():
            UserContribution.objects.create(
                user=request.user,
                initiative=initiative,
                contribution_details="Enrolled with no specific contribution yet."
            )
        return redirect('myApp:initiatives_list')  # Redirect back to the initiatives page


@login_required
def add_initiative(request):
    if request.method == 'POST':
        form = EnvironmentalInitiativeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Environmental initiative added successfully!')
            return redirect('myApp:initiatives_list')  # Change 'myApp:home' to your desired redirect URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EnvironmentalInitiativeForm()
    return render(request, 'myApp/add_initiative.html', {'form': form})


@login_required
def delete_initiative(request, initiative_id):
    initiative = get_object_or_404(EnvironmentalInitiative, id=initiative_id)
    if request.user.profile.is_recruiter:
        initiative.delete()
        messages.success(request, 'Initiative deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this initiative.')
    return redirect('myApp:initiatives_list')


@login_required
def delete_contribution(request, contribution_id):
    contribution = get_object_or_404(UserContribution, id=contribution_id)
    if request.user == contribution.user:
        contribution.delete()
        messages.success(request, 'You have successfully unenrolled from the initiative.')
    else:
        messages.error(request, 'You do not have permission to unenroll from this initiative.')
    return redirect('myApp:initiatives_list')