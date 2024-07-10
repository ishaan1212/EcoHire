# myApp/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class JobSearchForm(forms.Form):
    query = forms.CharField(label='Search Jobs', max_length=100)
class LoginForm(AuthenticationForm):
    ssn = forms.CharField(max_length=9, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
