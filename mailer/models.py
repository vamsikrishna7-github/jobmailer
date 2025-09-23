from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator


class UserProfile(models.Model):
    """Model to store comprehensive user profile information"""
    # Basic Information
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    primary_email = models.EmailField(max_length=255)
    
    # Contact Information
    alternative_email = models.EmailField(max_length=255, blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    github_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    leetcode_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    
    # Education
    education_degree = models.CharField(max_length=100)  # BTech, MTech, etc.
    education_field = models.CharField(max_length=255)  # Computer Science, etc.
    university_name = models.CharField(max_length=255)
    graduation_year = models.IntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    # Skills (stored as JSON-like text for flexibility)
    programming_languages = models.TextField(help_text="Comma-separated list")
    python_frameworks = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    frontend_technologies = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    mobile_development = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    databases = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    cloud_devops = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    deployment_platforms = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    integrations = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    development_practices = models.TextField(help_text="Comma-separated list", blank=True, null=True)
    
    # Professional Experience
    professional_experience = models.TextField(help_text="JSON format or structured text")
    
    # Projects
    projects = models.TextField(help_text="JSON format or structured text")
    
    # Resume file
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.education_degree} in {self.education_field}"


class EmailRequest(models.Model):
    """Model to store email generation requests"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='email_requests', blank=True, null=True)
    # Legacy fields for backward compatibility
    name = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    hr_email = models.EmailField(max_length=255)
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True, help_text="Optional job description")
    generated_email = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name = self.user_profile.name if self.user_profile else self.name
        return f"Email request for {name} at {self.company}"


class EmailSent(models.Model):
    """Model to track sent emails"""
    email_request = models.ForeignKey(EmailRequest, on_delete=models.CASCADE, related_name='sent_emails', blank=True, null=True)
    to_email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=500)
    body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='sent')
    resume_attached = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Email sent to {self.to_email} - {self.subject}"
