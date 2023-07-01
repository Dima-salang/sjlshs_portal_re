from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Request(models.Model):
    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='media/form_requests')

    def __str__(self) -> str:
        return self.name
    

class GoodMoral(models.Model):
    class Meta:
        verbose_name = "Good Moral Request"
        verbose_name_plural = "Good Moral Requests"

    purpose_choices = [
        ('college', "College Admissions"),
        ('scholarship', 'Scholarship Applications'),
        ('transfer', 'Transferring to Other School')
    ]
    
    full_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grade_level = models.CharField(max_length=2, null=True)
    lrn = models.CharField(max_length=15, null=True)
    residence = models.CharField(max_length=255, null=True)
    contact = models.CharField(max_length=11, null=True)
    email = models.EmailField(null=True)
    years_stayed = models.CharField(max_length=20, null=True)
    purpose = models.CharField(max_length=20, choices=purpose_choices, null=True)


    reasons = models.TextField(null=True, blank=True)
    plans = models.TextField(null=True, blank=True)
    transferring_school = models.CharField(max_length=50, null=True, blank=True)
    transferring_strand = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    

    def __str__(self) -> str:
        return f"{self.lrn}"
