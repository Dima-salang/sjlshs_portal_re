from django.urls import path
from .views import get_events


urlpatterns = [
    path('portal-calendar/get_events/', get_events, name='get-calendar-events')
]