from django import forms
from django.core.validators import FileExtensionValidator

from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'is_active']


class ApplicationForm(forms.ModelForm):
    resume = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']