from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def job_list_view(request):
    job_list = Job.objects.filter(is_active=True)
    paginator = Paginator(job_list, 5)

    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Prevent employers from applying
    if request.user.is_employer:
        messages.error(request, "Employers cannot apply to jobs.")
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        # Prevent duplicate applications
        if Application.objects.filter(job=job, seeker=request.user).exists():
            messages.warning(request, "You have already applied to this job.")
            return redirect('job_detail', job_id=job.id)

        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.seeker = request.user
            application.job = job
            application.save()
            messages.success(request, "Your application was submitted successfully.")
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})
