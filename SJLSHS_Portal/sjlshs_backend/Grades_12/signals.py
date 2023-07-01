from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import StudentUser
from .models import *


"""
The signals defined here are the same for the grade 11. Please refer to that module for more information.
"""

@receiver(pre_save, sender=FirstSem_1stQ)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass


@receiver(post_save, sender=FirstSem_1stQ)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = 'Grade Updated'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  PR2: {instance.PR2}
                  CPAR: {instance.CPAR}
                  PHILOSOPHY: {instance.PHILOSOPHY}
                  UCSP: {instance.UCSP}
                  EAPP: {instance.EAPP}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  PE: {instance.PE}
                  Average: {instance.Average}
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 1st quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Practical Research 2 : {instance.PR2}
                    Contemporary Arts Around the Regions : {instance.CPAR}
                    Introduction to the Philosophy of the Human Person: {instance.PHILOSOPHY}
                    Understanding Culture, Society, and Politics : {instance.UCSP}
                    English for Academic Purposes Program : {instance.EAPP}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALIZED_2}
                    Physical Education and Health 3 : {instance.PE}
                    """
    
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")




@receiver(pre_save, sender=FirstSem_2ndQ)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass



@receiver(post_save, sender=FirstSem_2ndQ)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  PR2: {instance.PR2}
                  CPAR: {instance.CPAR}
                  PHILOSOPHY: {instance.PHILOSOPHY}
                  UCSP: {instance.UCSP}
                  EAPP: {instance.EAPP}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  PE: {instance.PE}
                  Average: {instance.Average}
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 1st quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Practical Research 2 : {instance.PR2}
                    Contemporary Arts Around the Regions : {instance.CPAR}
                    Introduction to the Philosophy of the Human Person: {instance.PHILOSOPHY}
                    Understanding Culture, Society, and Politics : {instance.UCSP}
                    English for Academic Purposes Program : {instance.EAPP}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALIZED_2}
                    Physical Education and Health 3 : {instance.PE}
                    """
    
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")


@receiver(pre_save, sender=SecondSem_3rdQ)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass



@receiver(post_save, sender=SecondSem_3rdQ)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated for {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  III: {instance.III}
                  MIL: {instance.MIL}
                  PE4: {instance.PE4}
                  IMMERSION: {instance.IMMERSION}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  AVERAGE: {instance.Average}
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 1st quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Inquiries, Investigation, Immersion : {instance.III}
                    Media and Information Literacy : {instance.MIL}
                    Work Immersion : {instance.IMMERSION}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALIZED_2}
                    Physical Education and Health 4 : {instance.PE4}
                    """
    
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")


@receiver(pre_save, sender=SecondSem_4thQ)
def populate_student(sender, instance, **kwargs):
    try:
        student = StudentUser.objects.get(lrn=instance.lrn)
        instance.student = student
    except StudentUser.DoesNotExist:
        pass


@receiver(post_save, sender=SecondSem_4thQ)
def send_grade_update_email(sender, instance, **kwargs):
    print("Signal called")
    student_user = StudentUser.objects.get(lrn=instance.lrn)
    subject = f'Grade Updated for {instance.last_name}'
    message = f"""{instance.last_name}, {instance.first_name} - {instance.lrn}
                  Your grade is uploaded:
                  III: {instance.III}
                  MIL: {instance.MIL}
                  PE4: {instance.PE4}
                  IMMERSION: {instance.IMMERSION}
                  SPECIALIZED: {instance.SPECIALIZED}
                  SPECIALIZED: {instance.SPECIALIZED_2}
                  AVERAGE: {instance.Average}
                  """
    parent_message = f"""Greetings, we would like to notify you that the grades of {instance.last_name}, {instance.first_name} - {instance.lrn}
                    for the 1st quarter of the 1st semester is already complete. Here is the summary of their grades:
                    Inquiries, Investigation, Immersion : {instance.III}
                    Media and Information Literacy : {instance.MIL}
                    Work Immersion : {instance.IMMERSION}
                    Specialized Subject : {instance.SPECIALIZED}
                    Specialized Subject 2 : {instance.SPECIALIZED_2}
                    Physical Education and Health 4 : {instance.PE4}
                    """
    email_from = 'sjlshs.noreply@gmail.com'
    recipient_email = student_user.email
    parent_email = [student_user.parent_email]
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, parent_message, email_from, parent_email)
    print(f"Email sent to {recipient_list}")