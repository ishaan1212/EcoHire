from django.urls import path
from myApp.views import IndexView, JobDetailView

app_name = 'myApp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
]
