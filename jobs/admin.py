from django.contrib import admin
from .models import Job, Application


# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'seeker', 'applied_at')


admin.site.register(Job)
admin.site.register(Application, ApplicationAdmin)
