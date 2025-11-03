from datetime import date, timedelta
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
    
class TaskStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending',
    IN_PROGRESS = 'In Progress', 'In Progress',
    IN_REVIEW = 'In Review', 'In Review',
    COMPLETED = 'Completed', 'Completed'

class TaskPriority(models.TextChoices):
    HIGH = 'High', 'High',
    MEDIUM = 'Medium', 'Medium',
    LOW = 'Low', 'Low',

class Task(models.Model):
    """
    Represents a single unit of work associated with a Sample.
    This could be a synthesis step, a QC test, a purification, etc.
    This is the core of the "backlog".
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255, blank=False, null=False)
    
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    
    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM
    )
    
    due_date = models.DateField(null=True, blank=True)
    
    analyst = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,  # Allows for unassigned tasks
        blank=True, 
        related_name="tasks"
    )

    # Fields for results
    result_text = models.CharField(max_length=255, null=True, blank=True)
    result_numeric = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.sample.sample_id}"

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