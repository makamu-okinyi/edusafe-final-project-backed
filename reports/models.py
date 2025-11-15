# reports/models.py
# pylint: disable=no-member
import uuid
from django.db import models
from django.utils import timezone

def generate_case_id():
    """Generates a unique, human-readable case ID like ESC-2025-ABCD."""
    unique_part = uuid.uuid4().hex[:4].upper()
    current_year = timezone.now().year
    return f"ESC-{current_year}-{unique_part}"

class Report(models.Model):
    # Enum-like choices for status and category
    class StatusChoices(models.TextChoices):
        SUBMITTED = 'Submitted', 'Submitted'
        IN_REVIEW = 'Under Review', 'Under Review'
        IN_PROGRESS = 'Action in Progress', 'Action in Progress'
        RESOLVED = 'Resolved', 'Resolved'
        CLOSED = 'Closed', 'Closed'

    class CategoryChoices(models.TextChoices):
        BULLYING = 'Bullying', 'Bullying & Harassment'
        SAFETY = 'Safety', 'Safety & Security Concern'
        ACADEMIC = 'Academic', 'Academic Issue / Unfair Treatment'
        CONDUCT = 'Conduct', 'Teacher / Staff Conduct'
        NEGLECT = 'Neglect', 'Child Neglect or Abuse'
        OTHER = 'Other', 'Other Concern'

    # --- Model Fields ---
    case_id = models.CharField(max_length=20, unique=True, default=generate_case_id, editable=False)
    category = models.CharField(max_length=20, choices=CategoryChoices.choices)
    school_name = models.CharField(max_length=255)
    details = models.TextField()
    
    # Optional contact info
    reporter_name = models.CharField(max_length=255, blank=True, null=True)
    reporter_email = models.EmailField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.SUBMITTED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Django automatically adds get_category_display() for choice fields
        return f"Report {self.case_id} - {self.get_category_display()}"  # type: ignore[attr-defined]  # pylint: disable=no-member

class Evidence(models.Model):
    report = models.ForeignKey(Report, related_name='evidence_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # ForeignKey relationship allows access to related object attributes
        return f"Evidence for {self.report.case_id}"  # type: ignore[attr-defined]  # pylint: disable=no-member

class ReportMessage(models.Model):
    """
    A message related to a specific report, creating a chat thread.
    """
    class SenderTypeChoices(models.TextChoices):
        USER = 'User', 'User (Parent/Student)'
        AUTHORITY = 'Authority', 'Authority (Admin)'

    report = models.ForeignKey(Report, related_name='messages', on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SenderTypeChoices.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Django automatically adds get_sender_type_display() for choice fields
        # ForeignKey relationship allows access to related object attributes
        return f"Message from {self.get_sender_type_display()} on {self.report.case_id}"  # type: ignore[attr-defined]  # pylint: disable=no-member


class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Show newest posts first


class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, related_name='replies', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply on: {self.post.title}"

    class Meta:
        ordering = ['created_at'] # Show oldest replies first (chronological)

class Resource(models.Model):
    class ResourceCategory(models.TextChoices):
        MENTAL_HEALTH = 'Mental Health', 'Mental Health & Counseling'
        LEGAL_AID = 'Legal Aid', 'Legal Aid'
        SUPPORT_GROUP = 'Support Group', 'Support Group'
        ONLINE_SAFETY = 'Online Safety', 'Online Safety'
        EMERGENCY = 'Emergency', 'Emergency Hotline'

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ResourceCategory.choices)
    phone = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name