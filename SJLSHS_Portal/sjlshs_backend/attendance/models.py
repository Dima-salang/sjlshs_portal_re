from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Attendance(models.Model):
    lrn = models.CharField(max_length=15, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    status = models.BooleanField()


