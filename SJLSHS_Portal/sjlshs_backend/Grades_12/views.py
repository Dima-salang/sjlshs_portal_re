from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from accounts.models import StudentYear
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


# Create your views here.
@user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists())
def GradeView(request):
    grades1st = FirstSem_1stQ.objects.filter(lrn=request.user.lrn)
    grades2nd = FirstSem_2ndQ.objects.filter(lrn=request.user.lrn)
    grades3rd = SecondSem_3rdQ.objects.filter(lrn=request.user.lrn)
    grades4th = SecondSem_4thQ.objects.filter(lrn=request.user.lrn)

    grades = {
        'grades1st' : grades1st,
        'grades2nd' : grades2nd,
        'grades3rd' : grades3rd,
        'grades4th' : grades4th
    }

    return render(request, 'portal-grades.html', grades)