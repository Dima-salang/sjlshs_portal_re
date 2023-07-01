from django.shortcuts import render
from .models import Attendance
from accounts.models import StudentSection

# Create your views here.
def section_attendance(request, section_id):
    if request.user.is_superuser:
        section = StudentSection.objects.all()
    elif request.user.groups.filter(name='Advisors').exists():
        section = StudentSection.objects.get(pk=section_id)
    else:
        section = None
    students = StudentSection.studentuser_set.all()
    context = {
        'section' : section,
        'students' : students,

    }

    return render(request, 'attendance/section_attendance.html', context)
