from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_otp import devices_for_user
from django.core.mail import send_mail, EmailMessage
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.forms import OTPTokenForm
from django.contrib.auth.signals import user_logged_in
from .models import Enrolled_Students, StudentUser, TeacherUser
from django.conf import settings


user = get_user_model()

@receiver(post_save, sender=StudentUser)
def get_matching_fields(sender, instance, created, **kwargs):
    print('called signal for registration')
    if created:

        try:
            enrolled_student = Enrolled_Students.objects.get(lrn=instance.lrn)
            matched_fields = []

            if enrolled_student.last_name == instance.last_name:
                matched_fields.append('Last Name')
            if enrolled_student.first_name == instance.first_name:
                matched_fields.append('First Name')
            if enrolled_student.email == instance.email:
                matched_fields.append('Email')
            if enrolled_student.parent_email == instance.parent_email:
                matched_fields.append('Parent Email')
            if enrolled_student.birthday == instance.birthday:
                matched_fields.append('Birthday')
            if enrolled_student.grade_year == instance.grade_year:
                matched_fields.append('Grade Year')
            if enrolled_student.enrollment_status == instance.enrollment_status:
                matched_fields.append('Enrollment Status')

            if matched_fields:
                message = f"""Hello, there is a new student who registered for MAPS.
                
                
                New User:                   Found Enrolled Student:
                {instance.lrn}              {enrolled_student.lrn}
                {instance.last_name}        {enrolled_student.last_name}
                {instance.first_name}       {enrolled_student.first_name}
                {instance.email}            {enrolled_student.email}
                {instance.parent_email}     {enrolled_student.parent_email}
                {instance.birthday}         {enrolled_student.birthday}
                {instance.grade_year}       {enrolled_student.grade_year}
                {instance.enrollment_status}{enrolled_student.enrollment_status}

                The following fields have matched for LRN {instance.lrn} - {instance.last_name}, {instance.first_name}: {matched_fields}."""
            else:
                message = f"""Hello, there is a new student who registered for MAPS.
                
                No fields matched for LRN {instance.lrn} - {instance.last_name}, {instance.first_name}"""
            send_to = ["luisgabrielle1026@gmail.com"]
            send_mail(f"NEW STUDENT VERIFICATION {instance.lrn}", message, 'sjlshs.noreply@gmail.com', send_to)
            print('sent mail')

        except Enrolled_Students.DoesNotExist:
            message = f"""Hello, there is a new student who registered for MAPS.
            
            Unfortunately, no enrolled student was found with LRN {instance.lrn}. Double-check the user if this is a trustworthy account.
            If not, kindly delete the account."""

            send_to = ['luisgabrielle1026@gmail.com']
            send_mail(f"NEW STUDENT VERIFICATION {instance.lrn}", message, 'sjlshs.noreply@gmail.com', send_to)
            print('sent mail, enrolled_student DNE')


@receiver(post_save, sender=TeacherUser)
def email_teacher_account(sender, instance, created, **kwargs):
    if created:
        print('called signal for sending email to teacher at creation')

        message = f"""Greetings {instance.first_name}, {instance.first_name},
        
        your account has been created for SJLSHS MAPS. Here are your account details:
        ID Number : {instance.teacher_id}
        Email Address : {instance.user_field.email}
        Username : {instance.user_field.username}
        Password : {instance.raw_password}

        Please use the given credentials for the preliminary activation of your account.
        Rest assured, the username and password can be changed at a later time.
        The process of system-generated credentials is only for security purposes only.

        Best regards,
        San Jose Litex Senior High School

        """

        send_to = [instance.user_field.email]
        subject = "Preliminary Account Activation"
        send_mail(subject, message, 'sjlshs.noreply@gmail.com', send_to)