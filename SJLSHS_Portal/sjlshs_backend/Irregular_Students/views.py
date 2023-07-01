from django.shortcuts import render
from .models import IrregularStudent, SubjectGrade
from accounts.models import EnrollmentStatus
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Q
# Create your views here.

@user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists())
def grades_view(request):
    # Retrieve the grades of the irregular students
    grades1st = SubjectGrade.objects.filter(student__in=IrregularStudent.objects.filter(student=request.user, academic_period='1Q1S'))
    grades2nd = SubjectGrade.objects.filter(student__in=IrregularStudent.objects.filter(student=request.user, academic_period='2Q1S'))
    grades3rd = SubjectGrade.objects.filter(student__in=IrregularStudent.objects.filter(student=request.user, academic_period='3Q2S'))
    grades4th = SubjectGrade.objects.filter(student__in=IrregularStudent.objects.filter(student=request.user, academic_period='4Q2S'))
    context = {
        'grades1st' : grades1st,
        'grades2nd' : grades2nd,
        'grades3rd' : grades3rd,
        'grades4th' : grades4th
    }
    # Render a template with the grades as context data
    return render(request, 'irregular-grades.html', context)
