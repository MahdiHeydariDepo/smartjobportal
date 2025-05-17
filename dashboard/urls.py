from django.urls import path
from . import views
from .views import (
    employer_dashboard,
    EmployerJobCreateView,
    EmployerJobUpdateView,
    EmployerJobDeleteView, seeker_dashboard, create_job, job_applications
)

urlpatterns = [
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/', employer_dashboard, name='employer_dashboard'),
    path('employer/job/add/', create_job, name='employer_job_create'),
    path('employer/job/<int:pk>/edit/', EmployerJobUpdateView.as_view(), name='employer_job_edit'),
    path('employer/job/<int:pk>/delete/', EmployerJobDeleteView.as_view(), name='employer_job_delete'),
    path('seeker/', seeker_dashboard, name='seeker_dashboard'),
    path('employer/<int:job_id>/applications/', job_applications, name='job-applications'),
]
