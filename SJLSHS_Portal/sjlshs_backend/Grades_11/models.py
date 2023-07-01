from django.db import models
from accounts.models import StudentUser

"""
This module defines four Django models that represent the grades of students
for different subjects and quarters of a school year.

Each model represents a table in the database and contains the following fields:
- last_name: a string that represents the last name of the student
- first_name: a string that represents the first name of the student
- lrn: a string that represents the Learner Reference Number (LRN) of the student
- student: a foreign key that references the StudentUser model, representing the student

Each model also has a method named `get_queryset` that returns a filtered queryset 
of instances based on the user's role. Superusers have access to all instances, 
while advisors can only see instances that correspond to students in their sections.

Models:
- FirstSem_1stQ_11: represents the grades of students for the first quarter of the first semester of grade 11
- FirstSem_2ndQ_11: represents the grades of students for the second quarter of the first semester of grade 11
- SecondSem_3rdQ_11: represents the grades of students for the third quarter of the second semester of grade 11
- SecondSem_4thQ_11: represents the grades of students for the fourth quarter of the second semester of grade 11
"""


# Create your models here.

class FirstSem_1stQ_11(models.Model):

    class Meta:
        verbose_name = '1st QUarter Grade'
        verbose_name_plural = '1st Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    ORALCOMM = models.SmallIntegerField(default=0, null=True, blank=True)
    KOMUNIKASYON = models.SmallIntegerField(default=0, null=True, blank=True)
    GENMATH = models.SmallIntegerField(default=0, null=True, blank=True)
    ELS = models.SmallIntegerField(default=0, null=True, blank=True)
    PERDEV = models.SmallIntegerField(default=0, null=True, blank=True)
    LITERATURE = models.SmallIntegerField(default=0, null=True, blank=True)
    PR1 = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.SET_NULL, null=True, related_name="firstsem1stq11")

    def __str__(self):
        return f"{self.last_name} - {self.lrn}"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.select_related('student__section')
        elif request.user.groups.filter(name="Advisors").exists():
            return queryset.filter(student__section__section_adviser=request.user.teacheruser).select_related('student__section')
        else:
            return queryset.none()

class FirstSem_2ndQ_11(models.Model):

    class Meta:
        verbose_name = '2nd Quarter Grade'
        verbose_name_plural = '2nd Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    ORALCOMM = models.SmallIntegerField(default=0, null=True, blank=True)
    KOMUNIKASYON = models.SmallIntegerField(default=0, null=True, blank=True)
    GENMATH = models.SmallIntegerField(default=0, null=True, blank=True)
    ELS = models.SmallIntegerField(default=0, null=True, blank=True)
    PERDEV = models.SmallIntegerField(default=0, null=True, blank=True)
    LITERATURE = models.SmallIntegerField(default=0, null=True, blank=True)
    PR1 = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.SET_NULL, null=True, related_name="firstsem2ndq11")

    def __str__(self):
        return f"{self.last_name} - {self.lrn}"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.select_related('student__section')
        elif request.user.groups.filter(name="Advisors").exists():
            return queryset.filter(student__section__section_adviser=request.user.teacheruser).select_related('student__section')
        else:
            return queryset.none()

class SecondSem_3rdQ_11(models.Model):

    class Meta:
        verbose_name = '3rd Quarter Grade'
        verbose_name_plural = '3rd Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    READING_WRITING = models.SmallIntegerField(default=0, null=True, blank=True)
    PAGBASA = models.SmallIntegerField(default=0, null=True, blank=True)
    STATS_PROB = models.SmallIntegerField(default=0, null=True, blank=True)
    PHYSCI = models.SmallIntegerField(default=0, null=True, blank=True)
    EMPOWERMENT = models.SmallIntegerField(default=0, null=True, blank=True)
    ENTREP = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE2 = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.SET_NULL, null=True, related_name="secondsem3rdq11")

    def __str__(self):
        return f"{self.last_name} - {self.lrn}"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.select_related('student__section')
        elif request.user.groups.filter(name="Advisors").exists():
            return queryset.filter(student__section__section_adviser=request.user.teacheruser).select_related('student__section')
        else:
            return queryset.none()

class SecondSem_4thQ_11(models.Model):

    class Meta:
        verbose_name = '4th Quarter Grade'
        verbose_name_plural = '4th Quarter Grades'
    
    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    READING_WRITING = models.SmallIntegerField(default=0, null=True, blank=True)
    PAGBASA = models.SmallIntegerField(default=0, null=True, blank=True)
    STATS_PROB = models.SmallIntegerField(default=0, null=True, blank=True)
    PHYSCI = models.SmallIntegerField(default=0, null=True, blank=True)
    EMPOWERMENT = models.SmallIntegerField(default=0, null=True, blank=True)
    ENTREP = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE2 = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.SET_NULL, null=True, related_name="secondsem4thq11")

    def __str__(self):
        return f"{self.last_name} - {self.lrn}" 


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.select_related('student__section')
        elif request.user.groups.filter(name="Advisors").exists():
            return queryset.filter(student__section__section_adviser=request.user.teacheruser).select_related('student__section')
        else:
            return queryset.none()  