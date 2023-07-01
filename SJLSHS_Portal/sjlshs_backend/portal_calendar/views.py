from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CalendarEvent
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from accounts.models import StudentSection
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

# Create your views here.

"""
This module contains views for the calendar app.

Includes:

CalendarView: A TemplateView that renders a calendar page.
get_events: A function-based view that returns a JsonResponse containing events for the current month.

"""

@user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists())
def get_events(request):
        print("called get_events function")
        today = timezone.now().date()
        print(f"Timezone : {today}")
        universal_section = StudentSection.objects.get(section='Universal')
        events = CalendarEvent.objects.filter(Q(
            event_start_date__month=today.month,
            section=request.user.section
        ) | Q(event_start_date__month=today.month,
              section=universal_section))
        event_list = []
        for event in events:
            event_dict = {
                'title': event.event_title,
                'start': str(event.event_start_date),
                'end': str(event.event_end_date),
                'description': event.event_description,
                'level': str(event.event_level)
            }
            event_list.append(event_dict)
            print(event_dict)
        return JsonResponse(event_list, safe=False)


