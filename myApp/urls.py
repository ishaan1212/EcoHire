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
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Add more paths for other pages as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


