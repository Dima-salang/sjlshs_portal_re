from django.urls import path
from .views import home_page, recent_links, career_center_view, faculty_staff_view, all_announcements_view

urlpatterns = [
    path('organizations/', home_page, name='student-orgs'),
    path('recent_links/', recent_links, name='recent_links'),
    path('career-center/', career_center_view, name='career-center'),
    path('faculty/', faculty_staff_view, name='faculty-view'),
    path('all-announcements/', all_announcements_view, name='all-announcements'),
]

    