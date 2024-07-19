from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'myApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.jobs, name='jobs'),
    path('addjobs/', views.addJob, name='Addjobs'),
    path('addCompany/', views.addCompany, name='AddCompany'),
    path('about_us/', views.about_us, name='about_us'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('job-list/', views.jobs, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('manage_applications/', views.manage_applications, name='manage_applications'),
    path('update_application_review/<int:application_id>/', views.update_application_review, name='update_application_review'),
    # Add more paths for other pages as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


