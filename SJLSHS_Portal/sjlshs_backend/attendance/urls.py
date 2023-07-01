from django.urls import path
from .views import section_attendance

urlpatterns = [
    path('section_attendance/<int:section_id>', section_attendance, name='section_attendance'),
]