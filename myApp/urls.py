# myApp/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='myApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('search/', views.job_search, name='job-search'),
    path('contact/', views.contact_us_view, name='contact'),
    path('about/', views.about_us_view, name='about'),
    path('team/', views.team_details_view, name='team'),
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail')
]
