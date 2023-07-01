from django import forms
from .models import Post, Modules
from django.core.exceptions import ValidationError
from accounts.models import Subject, StudentYear


"""
This module defines two Django form classes that are used for filtering Module and CareerCenter objects.

ModuleFilterForm: 
A form class with the following fields:
- title_search: a CharField for searching for modules by title
- grade_level: a ModelChoiceField for filtering modules by grade level
- subject: a ModelChoiceField for filtering modules by subject

CareerCenterFilterForm:
A form class with the following field:
- school_search: a CharField for searching for career centers by school name

"""

class ModuleFilterForm(forms.Form):
    title_search = forms.CharField(required=False, label="Title")
    grade_level = forms.ModelChoiceField(StudentYear.objects.all(), label='Grade Level', required=False)
    subject = forms.ModelChoiceField(Subject.objects.all(), label='Subject', required=False)


class CareerCenterFilterForm(forms.Form):
    school_search = forms.CharField(required=False, label="School", help_text="Search for the name of the school")