from django.db import models
from accounts.models import StudentUser

# Create your models here.

"""
The documentation for Grade 12 models is the same for the Grade 11. Refer to that module
for more information.
"""

class FirstSem_1stQ(models.Model):

    class Meta:
        verbose_name = '1st Quarter Grade'
        verbose_name_plural = '1st Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    PR2 = models.SmallIntegerField(default=0, null=True, blank=True)
    CPAR = models.SmallIntegerField(default=0, null=True, blank=True)
    PHILOSOPHY = models.SmallIntegerField(default=0, null=True, blank=True)
    UCSP = models.SmallIntegerField(default=0, null=True, blank=True)
    EAPP = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.CASCADE, null=True, related_name="firstsem1stq")

    def __str__(self):
        return f"{self.last_name} - {self.lrn}"
    

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(queryset)
        if request.user.is_superuser:
            filtered = queryset.select_related('student__section')
            print(filtered)
            return filtered
        elif request.user.groups.filter(name="Advisors").exists():
            filtered_queryset = queryset.filter(student__section__section_adviser=request.user.teacheruser).select_related('student__section')
            print(filtered_queryset)
            return filtered_queryset
        else:
            return queryset.none()

class FirstSem_2ndQ(models.Model):

    class Meta:
        verbose_name = '2nd Quarter Grade'
        verbose_name_plural = '2nd Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    PR2 = models.SmallIntegerField(default=0, null=True, blank=True)
    CPAR = models.SmallIntegerField(default=0, null=True, blank=True)
    PHILOSOPHY = models.SmallIntegerField(default=0, null=True, blank=True)
    UCSP = models.SmallIntegerField(default=0, null=True, blank=True)
    EAPP = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    PE = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.CASCADE, null=True, related_name="firstsem2ndq")

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

class SecondSem_3rdQ(models.Model):

    class Meta:
        verbose_name = '3rd Quarter Grade'
        verbose_name_plural = '3rd Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    III = models.SmallIntegerField(default=0, null=True, blank=True)
    MIL = models.SmallIntegerField(default=0, null=True, blank=True)
    PE4 = models.SmallIntegerField(default=0, null=True, blank=True)
    IMMERSION = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.CASCADE, null=True, related_name="secondsem3rdq")

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

class SecondSem_4thQ(models.Model):

    class Meta:
        verbose_name = '4th Quarter Grade'
        verbose_name_plural = '4th Quarter Grades'

    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    III = models.SmallIntegerField(default=0, null=True, blank=True)
    MIL = models.SmallIntegerField(default=0, null=True, blank=True)
    PE4 = models.SmallIntegerField(default=0, null=True, blank=True)
    IMMERSION = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED = models.SmallIntegerField(default=0, null=True, blank=True)
    SPECIALIZED_2 = models.SmallIntegerField(default=0, null=True, blank=True)
    Average = models.IntegerField(default=0, null=True, blank=True)
    lrn = models.CharField(max_length=15)
    student = models.OneToOneField(StudentUser, on_delete=models.CASCADE, null=True, related_name="secondsem4thq")

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