from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Job, Company, Application, Profile
from django.contrib.auth.forms import AuthenticationForm
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
        fields = ['user', 'country', 'phone_number', 'gender']


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

    job_type = forms.ChoiceField(required=False, choices=[('', 'Choose a category...')] + list(Job.JOB_TYPE_CHOICES), widget=forms.Select(attrs={
        'class': 'search-select'
    }))


COUNTRIES = [
    ("AF", "+93 Afghanistan"),
    ("AL", "+355 Albania"),
    ("DZ", "+213 Algeria"),
    # Add more countries here...
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    country = forms.ChoiceField(choices=COUNTRIES, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    is_recruiter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'gender', 'password1', 'password2', 'is_recruiter')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.country = self.cleaned_data['country']
            profile.gender = self.cleaned_data['gender']
            profile.is_recruiter = self.cleaned_data['is_recruiter']  # Ensure this is saved
            profile.save()
        return user


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        fields = ['username', 'password', 'remember_me']