from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import StudentUser
from .models import *
from django.conf import settings

"""
This module defines signal receivers for updating student grades and sending email notifications in response to model saves. It imports the following Django modules:
- `send_mail` from `django.core.mail`
- `post_save` and `pre_save` from `django.db.models.signals`
- `receiver` from `django.dispatch`
- `settings` from `django.conf`

It also imports the `StudentUser` and model classes from the `accounts.models` and the current directory. The signal receivers are as follows:
- `populate_student`: before saving an instance of any of the `FirstSem_1stQ_11`, `FirstSem_2ndQ_11`, `SecondSem_3rdQ_11`, and `SecondSem_4thQ_11` models, set its `student` field to the corresponding `StudentUser` instance with the same `lrn` attribute.
- `send_grade_update_email`: after saving an instance of any of the `FirstSem_1stQ_11`, `FirstSem_2ndQ_11`, `SecondSem_3rdQ_11`, and `SecondSem_4thQ_11` models, send an email to the corresponding `StudentUser` instance with the updated grade information.
"""

@receiver(pre_save, sender=FirstSem_1stQ_11)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass


@receiver(post_save, sender=FirstSem_1stQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated for {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Greetings from SJLSHS! Your grade for the first semester, first quarter has been uploaded.
                  Log in to the portal to see your grades and for more information.
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 1st quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Oral Communication : {instance.ORALCOMM}
                    Komunikasyon at Pananaliksik : {instance.KOMUNIKASYON}
                    General Mathematics : {instance.GENMATH}
                    Earth and Life Science : {instance.ELS}
                    Personal Development : {instance.PERDEV}
                    21st Century Literature : {instance.LITERATURE}
                    Practical Research 1 : {instance.PR1}
                    Specialized Subject : {instance.SPECIALIZED}
                    
                    Physical Education and Health : {instance.PE}
                    """
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    
    parent_email = [student_user.parent_email]

    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    print(f"Email sent to {recipient_list}")
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {parent_email}")


@receiver(pre_save, sender=FirstSem_2ndQ_11)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass

@receiver(post_save, sender=FirstSem_2ndQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated for {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Greetings from SJLSHS! Your grade for the first semester, second quarter has been uploaded.
                  Log in to the portal to see your grades and for more information.
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 2nd quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Oral Communication : {instance.ORALCOMM}
                    Komunikasyon at Pananaliksik : {instance.KOMUNIKASYON}
                    General Mathematics : {instance.GENMATH}
                    Earth and Life Science : {instance.ELS}
                    Personal Development : {instance.PERDEV}
                    21st Century Literature : {instance.LITERATURE}
                    Practical Research 1 : {instance.PR1}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALZED_2}
                    Physical Education and Health : {instance.PE}
                    """
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")


@receiver(pre_save, sender=SecondSem_3rdQ_11)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass

@receiver(post_save, sender=SecondSem_3rdQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Greetings from SJLSHS! Your grade for the second semester, third quarter has been uploaded.
                  Log in to the portal to see your grades and for more information.
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 3rd quarter of the 2nd semester is already complete. Here is the summary of their grades:
                    Reading and Writing : {instance.READING_WRITING}
                    Pagbasa at Pagsusuri ng Iba't Ibang Teksto Tungo sa Pananaliksik : {instance.PAGBASA}
                    Statistics and Probability : {instance.STATS_PROB}
                    Physical Science : {instance.PHYSCI}
                    Empowerment Technologies : {instance.EMPOWERMENT}
                    Entrepreneurship : {instance.ENTREP}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALZED_2}
                    Physical Education and Health 2 : {instance.PE}
                    """
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")


@receiver(pre_save, sender=SecondSem_4thQ_11)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass

@receiver(post_save, sender=SecondSem_4thQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    if kwargs.get('created', False):
        return
    subject = f'Grade Updated for {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Greetings from SJLSHS! Your grade for the second semester, fourth quarter has been uploaded.
                  Log in to the portal to see your grades and for more information.
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 4th quarter of the 2nd semester is already complete. Here is the summary of their grades:
                    Reading and Writing : {instance.READING_WRITING}
                    Pagbasa at Pagsusuri ng Iba't Ibang Teksto Tungo sa Pananaliksik : {instance.PAGBASA}
                    Statistics and Probability : {instance.STATS_PROB}
                    Physical Science : {instance.PHYSCI}
                    Empowerment Technologies : {instance.EMPOWERMENT}
                    Entrepreneurship : {instance.ENTREP}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALZED_2}
                    Physical Education and Health 2 : {instance.PE}
                    """
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")
























@receiver(post_save, sender=SecondSem_3rdQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    if kwargs.get('created', False):
        return
    subject = 'Grade Updated'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  READING AND WRITING {instance.READING_WRITING}
                  PAGBASA {instance.PAGBASA}
                  STATISTICS AND PROBABILITY {instance.STATS_PROB}
                  PHYSICAL SCIENCE {instance.PHYSCI}
                  EMPOWERMENT TECHNOLOGIES {instance.EMPOWERMENT}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  PHYSICAL AND EDUCATION 2: {instance.PE2}
                  Average: {instance.Average}
                  """
    email_from = "SJLSHS@gmail.com"
    recipient_email = student_user.email
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    print(f"Email sent to {recipient_list}")

@receiver(post_save, sender=SecondSem_4thQ_11)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    if kwargs.get('created', False):
        return
    subject = 'Grade Updated'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  READING AND WRITING {instance.READING_WRITING}
                  PAGBASA {instance.PAGBASA}
                  STATISTICS AND PROBABILITY {instance.STATS_PROB}
                  PHYSICAL SCIENCE {instance.PHYSCI}
                  EMPOWERMENT TECHNOLOGIES {instance.EMPOWERMENT}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  PHYSICAL AND EDUCATION 2: {instance.PE2}
                  Average: {instance.Average}
                  """
    email_from = "SJLSHS@gmail.com"
    recipient_email = student_user.email
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    print(f"Email sent to {recipient_list}")


