from django.urls import path
from .views import grades_view

urlpatterns = [
    path('grades/', grades_view, name='irregular-grades'),
]
