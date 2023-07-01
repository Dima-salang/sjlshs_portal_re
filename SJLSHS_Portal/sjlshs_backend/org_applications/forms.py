from django import forms
from .models import Organization, OrganizationApplication
from django.contrib.auth import get_user_model
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

User = get_user_model()

class OrganizationApplicationForm(forms.ModelForm):


    class Meta:
        model = OrganizationApplication
        exclude = ['applicant', 'date_submitted']
        widgets = {
            'application_letter' : SummernoteWidget() 
        }

    