from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import CalendarEvent
from accounts.models import StudentUser, StudentSection


students = StudentUser.objects.all()

@shared_task
def check_upcoming_events():
    today = timezone.now().date()
    deadline_limit = today + timezone.timedelta(days=7)
    upcoming_deadlines = CalendarEvent.objects.filter(
        event_start_date__gte=today,
        event__start_date__lte=deadline_limit,
    )

    for event in upcoming_deadlines:
        subject = f"Upcoming: {event.event_title}"
        message = f"""Hello,

        This is a reminder that {event.event_title} is coming up on {event.event_end_date}.
        Be sure to log-in in the SJLSHS MAPS for more information about the event.

        Best regards,
        San Jose Litex Senior High School
        """

        if event.section == StudentSection.objects.get(section="Universal"):
            student_emails = [student.email for student in StudentUser.objects.all()]
        else:
            student_emails = [student.email for student in StudentUser.objects.filter(section__in=event.section.all())]
        
        send_mail(subject, message, "SJLSHS@gmail.com", student_emails)
