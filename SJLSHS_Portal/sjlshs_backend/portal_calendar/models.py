from django.db import models
from accounts.models import StudentSection

# Create your models here.


class EventLevel(models.Model):
    level = models.CharField(max_length=20)


class CalendarEvent(models.Model):

    CALENDAR_CHOICES = [
        ("IMPORTANT", "IMPORTANT"),
        ("REMINDER", "REMINDER")
    ]

    class Meta:
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    author = models.CharField(max_length=100, null=True)
    event_title = models.CharField(max_length=100)
    event_description = models.TextField()
    event_start_date = models.DateField(null=True)
    event_end_date = models.DateField(null=True)
    event_level = models.CharField(max_length=20, choices=CALENDAR_CHOICES, null=True)
    section = models.ManyToManyField(StudentSection, null=True)

    def __str__(self) -> str:
        return f"{self.event_title} - {self.event_level}"
