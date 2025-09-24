from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class UserType(models.TextChoices):
        CANDIDATE = 'candidate', _('Candidate')
        EMPLOYER = 'employer', _('Employer')
        ADMIN = 'admin', _('Admin')

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    user_type = models.CharField(max_length=16, choices=UserType.choices, default=UserType.CANDIDATE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email or self.username


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(
        upload_to='resumes/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name='profiles')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile<{self.user_id}> {self.user.email}"


class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.degree} @ {self.institution}"


class Experience(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} @ {self.company_name}"


class Project(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class SocialLinks(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='social_links')
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    leetcode = models.URLField(blank=True)
    codeforces = models.URLField(blank=True)
    others = models.TextField(blank=True)

    def __str__(self):
        return f"Links<{self.profile_id}>"


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class BasicInfo(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='basic_info')
    preferred_location = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    alternate_email = models.EmailField(blank=True)
    alternate_phone = models.CharField(max_length=32, blank=True)
    address = models.TextField(blank=True)
    email_app_user = models.EmailField(blank=True, help_text='Email ID associated with app password')
    email_app_password = models.CharField(max_length=255, blank=True, help_text='App password for outbound email')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BasicInfo<{self.profile_id}>"

# Create your models here.
