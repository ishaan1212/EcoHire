from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from myApp.forms import ProfileForm, UserRegistrationForm, JobPostForm
from myApp.models import Job


# Create your views here.


def home(request):
    return render(request, 'myApp/home.html')


def jobs(request):
    jobs_lists = Job.objects.all()
    context = {
        'title': 'Jobs Page',
        'jobs_lists': jobs_lists,
    }
    return render(request, 'myApp/jobs.html', context)


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



#@login_required
def post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            return redirect('myApp:jobs')
    else:
        form = JobPostForm()
    return render(request, 'myApp/post.html', {'form': form})



