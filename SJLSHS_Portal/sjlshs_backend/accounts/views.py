from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login 
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.urls import reverse_lazy, reverse
from django.views import generic
from django import forms
from .forms import CustomCreationForm, StudentInfoForm, TeacherCreationForm, TeacherLogInForm, TeacherChangeDetailsForm, ResetPasswordForm
from .models import StudentUser, TeacherUser, PasswordResetToken
from .auth_backends import TeacherAuthenticationBackend
from django.dispatch import receiver
from django.contrib import messages
from django_otp import devices_for_user
from two_factor.views import LoginView, OTPRequiredMixin, SetupView
from secrets import choice
from django.contrib.auth.decorators import user_passes_test
from string import ascii_letters, digits as num_digits
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
# Create your views here.


User = get_user_model()

class SignUpView(generic.CreateView):
    """
    This contains a view for user sign up functionality, which allows users to create a new account 
    on the platform. It uses a CustomCreationForm form for user registration and sends an activation
      email to the user for email verification.

    Classes:

    SignUpView: A class-based view that inherits from Django's generic CreateView. 
    It uses a CustomCreationForm form for user registration and sends an activation 
    email to the user for email verification.

    Functions:

    activate: A view function for activating the user's email verification link. 
    It decodes the user's id and token from the URL and verifies the token using the 
    account_activation_token instance of TokenGenerator class. If the token is valid, 
    it sets the is_email_verified field of the user to True and redirects to
    """


    form_class = CustomCreationForm
    success_url = reverse_lazy('signup-redirect')
    template_name = 'signup.html'

    def form_valid(self, form):

        if form.is_valid():
            lrn = form.cleaned_data.get('lrn')
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            curr_site = get_current_site(self.request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                'user': user,
                'domain': curr_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return super().form_valid(form)


    def activate(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            pass
        if user is not None and account_activation_token.check_token(user,token):
            user.is_email_verified= True
            user.save()
            return redirect('two_factor:login')
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['signup_modal_shown'] = not self.request.COOKIES.get('signup_modal_shown', False)
        return context
        

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.COOKIES.get('signup_modal_shown', False):
            expiration_time = datetime.now() + timedelta(hours=1)
            response.set_cookie('signup_modal_shown', True, expires=expiration_time)
        return response

class SignUpRedirectView(generic.TemplateView):
    template_name = 'signup-redirect.html'
                    

# deprecated... removed dashboard view for teachers. Moved to admin site.                   
def TeacherDashboardView(request):
    students = StudentUser.objects.exclude(groups__name__in=['Teachers'])
    context = {
        'students' : students
    }

    return render(request, 'tc-dashboard.html', context)


def StudentInfoView(request, uid):
    student = StudentUser.objects.get(id=uid)
    form = StudentInfoForm(instance=student)
    if request.method == 'POST':
        form = StudentInfoForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            redirect('accounts/teachers/dashboard')
    contexts = {
        'form' : form
    }

    return render(request, 'tc-student-info.html', contexts)


        
# overrides get_success_url for SetUpView of two_factor
class CustomSetupView(SetupView):
    success_url = reverse_lazy('two_factor:login') # redirect to login page after successful setup

    def get_success_url(self):
        print(self.success_url)
        return self.success_url
    

class TeacherRegistrationView(generic.FormView):
    form_class = TeacherCreationForm
    template_name = 'registration/teacher.html'
    success_url = reverse_lazy('admin:index')

    def form_valid(self, form):
        alphabet = ascii_letters + num_digits
        self.sys_pass = ''.join(choice(alphabet) for i in range(15))
        print('form_valid method called')
        if form.is_valid():
            user = form.save(commit=False)
            user.lrn = f"DepEd_{user.lrn}"
            user.username = f"DepEd_{user.username}"
            user.set_password(self.sys_pass)
            print(user)
            user.save()
            teacher_user = TeacherUser.objects.create(
                user_field=user,
                teacher_id=user.lrn,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                raw_password = self.sys_pass
            )
            print(teacher_user)
            teacher_user.save()
            return super().form_valid(form)
    

class TeacherLogInView(generic.FormView):
    form_class = TeacherLogInForm
    template_name = 'login/teacher_login.html'
    success_url = reverse_lazy('admin:index')

    def form_valid(self, form):
        # Authenticate user
        teacher_id = form.cleaned_data['teacher_id']
        print(teacher_id)
        username = form.cleaned_data['username']
        print(username)
        password = form.cleaned_data['password']
        print(password)
        user = authenticate(
            username=username, password=password
        )
        if user is None:
            raise forms.ValidationError(
                "Invalid login credentials. Please try again.",
                code='invalid_login'
            )


        return redirect(reverse_lazy('admin:index'))



def teacher_change_details(request):
    if request.method == 'POST':
        form = TeacherChangeDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your details have been updated successfully!')
            return redirect('teacher-update-password')
    else:
        form = TeacherChangeDetailsForm(instance=request.user)
    return render(request, 'registration/change_details.html', {'form': form})


class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('admin:index')
    template_name = 'registration/update_password.html'




def forgot_password_view(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        username = request.POST['username']
        user = User.objects.get(lrn=user_id, username=username)
        if user:
            # generate token
            token = str(uuid.uuid4())
            token_expiration = timezone.now() + timezone.timedelta(hours=1)

            user_reset = PasswordResetToken.objects.create(
                student=user,
                password_token=token,
                password_token_expiration=token_expiration
            )

            user_reset.save()

            reset_url = request.build_absolute_uri(reverse('reset_password', args=[token]))
            message = f"Click on the following link to reset your password: {reset_url}"
            send_mail(
                "Password Reset",
                message,
                from_email='SJLSHS@gmail.com',
                recipient_list=[user.email],
                fail_silently=False
            )

            return render(request, 'login/password_reset_sent_email.html')
        else:
            return render(request, 'login/forgot_password.html', {'error' : 'Invalid LRN or Username'})
        
    else:
        return render(request, 'login/forgot_password.html')



def reset_password(request, token):
    # Get the password reset token
    password_reset_token = get_object_or_404(PasswordResetToken, password_token=token)

    # Check if the token has expired
    if timezone.now() > password_reset_token.password_token_expiration:
        return render(request, 'login/password_reset_token_expired.html')

    # Get the user associated with the password reset token
    user = password_reset_token.student
    print(user)
    form = ResetPasswordForm(user)

    if request.method == 'POST':
        # Validate the password reset form
        form = ResetPasswordForm(request.POST)
        print(form)
        if form.is_valid():
            print('form valid')
            # Update the user's password
            user.set_password(form.cleaned_data['new_password'])
            print("Changed password")
            user.save()

            # Delete the password reset token
            password_reset_token.delete()

            return render(request, 'login/password_reset_successful.html')
        else:
            print(form.errors)
    else:
        print("reset")
        
        
        

    return render(request, 'login/reset_password.html', {'form': form})