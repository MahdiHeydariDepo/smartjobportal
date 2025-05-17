from django.urls import path
from .views import job_list_view, apply_to_job, job_detail

urlpatterns = [
    path('', job_list_view, name='job-list'),
    path('<int:job_id>/apply/', apply_to_job, name='apply-to-job'),
    path('<int:job_id>/', job_detail, name='job_detail'),
]
