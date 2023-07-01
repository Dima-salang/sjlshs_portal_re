from django import forms
from wagtail.admin.forms.auth import LoginForm
from captcha.fields import CaptchaField
from django_otp import forms as otp_forms

class LRNAuthenticationForm(LoginForm, otp_forms.AuthenticationForm):
    lrn = forms.CharField(max_length=100, required=True)
    captcha = CaptchaField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('otp_token', None)
        self.fields.pop('otp_challenge', None)