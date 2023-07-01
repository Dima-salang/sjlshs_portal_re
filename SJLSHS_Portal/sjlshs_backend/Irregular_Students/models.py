from django.db import models
from accounts.models import Subject, StudentUser

# Create your models here.

class IrregularStudent(models.Model):

    class Meta:
        verbose_name = 'Irregular Student'
        verbose_name_plural = 'Irregular Students'

    FIRST_QUARTER = "1Q1S"
    SECOND_QUARTER = "2Q1S"
    THIRD_QUARTER = "3Q2S"
    FOURTH_QUARTER = "4Q2S"
    ACADEMIC_PERIOD_CHOICES = [
        (FIRST_QUARTER, "First Quarter, 1st Semester"),
        (SECOND_QUARTER, "Second Quarter, 1st Semester"),
        (THIRD_QUARTER, "Third Quarter, 2nd Semester"),
        (FOURTH_QUARTER, "Fourth Quarter, 2nd Semester")
    ]
    name = models.CharField(max_length=100)
    student = models.ForeignKey(StudentUser, null=True, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='SubjectGrade')
    academic_period = models.CharField(max_length=4, choices=ACADEMIC_PERIOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.student.lrn} - {self.name}"

class SubjectGrade(models.Model):

    class Meta:
        verbose_name = 'Irregular Subject Grade'
        verbose_name_plural = 'Irregular Subject Grades'

    student = models.ForeignKey(IrregularStudent, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"