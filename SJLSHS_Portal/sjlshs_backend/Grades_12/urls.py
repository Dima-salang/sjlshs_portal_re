from django.urls import path
from . import views


urlpatterns = [
    path('portal-grades/12/', views.GradeView, name='portal-grade'),
]