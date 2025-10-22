from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SampleStatus(models.TextChoices):
    RECEIVED = 'Received', 'Received'
    PROCESSING = 'Processing', 'Processing'
    ANALYZED = 'Analyzed', 'Analyzed'
    COMPLETE = 'Complete', 'Complete'

class Sample(models.Model):
    """
    Represents a single laboratory sample.
    """
    sample_id = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="samples")
    status = models.CharField(
        max_length=20,
        choices=SampleStatus.choices,
        default=SampleStatus.RECEIVED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sample_id} ({self.name})"

class AuditLog(models.Model):
    """
    Tracks changes to a Sample for compliance and history.
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="audit_logs")
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="audit_action")
    action = models.TextField() # e.g., "Status changed from 'Processing' to 'Analyzed'."
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.sample.sample_id} at {self.timestamp}"