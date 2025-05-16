from django.urls import path
from .views import job_list_view, apply_to_job

urlpatterns = [
    path('', job_list_view, name='job-list'),
    path('<int:job_id>/apply/', apply_to_job, name='apply-to-job'),
]
