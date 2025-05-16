from django.contrib import admin
from .models import Job


# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'seeker', 'applied_at')


admin.site.register(Job)
