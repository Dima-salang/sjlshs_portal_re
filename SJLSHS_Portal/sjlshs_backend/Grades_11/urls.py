from django.urls import path
from . import views


urlpatterns = [
    path('portal-grade/11', views.GradeView, name='portal-grade11'),
]