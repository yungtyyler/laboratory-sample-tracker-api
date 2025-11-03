from django.contrib import admin
from .models import Task, AuditLog, Sample

# Register your models here.
admin.site.register(Task)
admin.site.register(AuditLog)
admin.site.register(Sample)