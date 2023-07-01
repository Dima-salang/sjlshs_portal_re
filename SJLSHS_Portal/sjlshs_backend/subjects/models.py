from django.db import models
from accounts.models import StudentSection

# Create your models here.

class CoreSubjects(models.Model):
    subject_matter = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.subject_matter}"

class SpecializedSubjects(models.Model):
    spec_sub = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.spec_sub}"
