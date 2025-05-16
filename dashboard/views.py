from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from jobs.models import Job, Application
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from jobs.forms import JobForm, ApplicationForm


# Employer-views********************
@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        return render(request, '403.html')  # Optional: handle unauthorized access

    jobs = Job.objects.filter(employer=request.user)
    applications = Application.objects.filter(job__in=jobs)

    return render(request, 'dashboard/employer/employer_dashboard.html', {
        'jobs': jobs,
        'applications': applications
    })


class EmployerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_employer


class EmployerJobListView(LoginRequiredMixin, EmployerRequiredMixin, ListView):
    model = Job
    template_name = 'dashboard/employer/employer_job_list.html'

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)


class EmployerJobCreateView(LoginRequiredMixin, EmployerRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'dashboard/employer/job_form.html'
    success_url = reverse_lazy('employer-jobs')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super().form_valid(form)


def create_job(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
    return render(request, 'dashboard/employer/job_form.html', {'form': form})


class EmployerJobUpdateView(LoginRequiredMixin, EmployerRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'dashboard/employer/job_form.html'
    success_url = reverse_lazy('employer-jobs')

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)


class EmployerJobDeleteView(LoginRequiredMixin, EmployerRequiredMixin, DeleteView):
    model = Job
    template_name = 'dashboard/employer/job_confirm_delete.html'
    success_url = reverse_lazy('employer-jobs')

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)


# Seeker-views********************

def seeker_dashboard(request):
    if not request.user.is_seeker:
        return render(request, 'dashboard/access_denied.html')

    applications = Application.objects.filter(seeker=request.user).select_related('job')
    return render(request, 'dashboard/seeker/seeker_dashboard.html', {
        'applications': applications
    })
