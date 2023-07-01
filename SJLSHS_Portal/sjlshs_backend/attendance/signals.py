from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Attendance


User = get_user_model()

@receiver(post_save, sender=Attendance)
def populate_student(sender, instance, **kwargs):
    try:
        student = User.objects.get(lrn=instance.lrn)
        instance.student = student
    except User.DoesNotExist:
        pass
    