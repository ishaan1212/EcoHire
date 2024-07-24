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
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('job-list/', views.jobs, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('manage_applications/', views.manage_applications, name='manage_applications'),
    path('update_application_review/<int:application_id>/', views.update_application_review, name='update_application_review'),
    path('initiatives/', views.initiatives_list, name='initiatives_list'),
    path('contributions/', views.user_contributions, name='user_contributions'),
    path('enroll-initiative/<int:initiative_id>/', views.enroll_initiative, name='enroll_initiative'),
    path('add_initiative/', views.add_initiative, name='add_initiative'),
    path('delete_initiative/<int:initiative_id>/', views.delete_initiative, name='delete_initiative'),
    path('delete_contribution/<int:contribution_id>/', views.delete_contribution, name='delete_contribution'),
    path('faq/submit/', views.faq_submission, name='faq_submission'),
    path('faqs/', views.faq_list, name='faq_list'),
    path('faq/<int:faq_id>/answer/', views.answer_faq, name='answer_faq'),
    path('eco-survey/<int:company_id>/', views.eco_survey, name='eco-survey'),
    path('select-company/', views.select_company_for_eco_verification, name='select_company'),
    path('get-companies/', views.get_companies, name='get_companies'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    # Add more paths for other pages as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


