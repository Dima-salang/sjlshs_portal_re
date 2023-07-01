from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from form_requests.models import GoodMoral


@receiver(post_save, sender=GoodMoral)
def send_guidance_mail(sender, instance, created, **kwargs):
    print("called signal for guidance")
    if created:
        message = f"Hello, Guidance Counselor, {instance.full_name}, {instance.lrn} has requested a certificate of good moral."
        send_to = ["luisgabrielle1026@gmail.com",]
        send_mail("Request for Good Moral", message, "sjlshs.noreply@gmail.com", send_to)

