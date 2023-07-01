from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import TeacherUser

# Create your models here.

User = get_user_model()

class Organization(models.Model):
    organization_logo = models.ImageField(upload_to='media/orgs_logo', null=True, verbose_name='Organization Logo')
    organization_name = models.CharField(max_length=100, null=True)
    adviser = models.ForeignKey(TeacherUser, on_delete=models.CASCADE, null=True, blank=True, related_name='org_adviser')
    president = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='org_president')
    short_description = models.TextField(null=True)
    organization_wagtail_url = models.URLField(null=True)

    def __str__(self) -> str:
        return f"{self.organization_name}"

class OrganizationApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, verbose_name="Choice of Organization")
    application_letter = models.TextField(null=True, verbose_name="Application Letter",
                                           help_text="Please provide a brief summary of why you want to join the organization, your goals and missions, and how you would like to contribute.")
    date_submitted = models.DateField(auto_now=True, null=True)

    def __str__(self) -> str:
        return f"{self.applicant}-{self.organization}"
    
