from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Job, Company, Application, Profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'job_type', 'location', 'description', 'requirements', 'responsibilities', 'salary','currency']

        CURRENCY_CHOICES = [
            ('USD', 'USD'),
            ('EUR', 'EUR'),
            ('GBP', 'GBP'),
            ('CAD', 'CAD'),
            ('INR', 'INR')
        ]

        currency = forms.ChoiceField(choices=CURRENCY_CHOICES, label='Currency')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'website', 'description']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['user', 'job', 'company', 'resume', 'cover_letter', 'status']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'phone_number', 'address', 'city', 'country', 'date_of_birth']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class JobSearchForm(forms.Form):
    keywords = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Keywords',
        'class': 'search-input'
    }))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Location',
        'class': 'search-input'
    }))
    job_type = forms.ChoiceField(required=False, choices=[('', 'Choose a category...')] + list(Job.JOB_TYPE_CHOICES), widget=forms.Select(attrs={
        'class': 'search-select'
    }))