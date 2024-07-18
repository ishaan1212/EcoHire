from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Job, Company, Application, Profile, ApplicationReview


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'job_type', 'location', 'description', 'requirements', 'responsibilities',
                  'salary', 'currency']

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
        fields = ['job', 'company', 'user', 'resume', 'cover_letter', 'motivation_letter', 'experience', 'skills', 'status']
        widgets = {
            'status': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'motivation_letter': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        job = kwargs.pop('job', None)
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].disabled = True
        if job:
            self.fields['job'].initial = job.pk
            self.fields['job'].disabled = True
        if company:
            self.fields['company'].initial = company.pk
            self.fields['company'].disabled = True
        self.fields['status'].initial = 'P'  # Ensure status is set to 'Pending'
        self.fields['status'].disabled = True

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
    job_type = forms.ChoiceField(required=False, choices=[('', 'Choose a category...')] + list(Job.JOB_TYPE_CHOICES),
                                 widget=forms.Select(attrs={
                                     'class': 'search-select'
                                 }))

class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = ApplicationReview
        fields = ['status', 'comments']
