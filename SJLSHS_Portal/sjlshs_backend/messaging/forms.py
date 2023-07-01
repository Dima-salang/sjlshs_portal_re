from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Message, Reply
from accounts.models import StudentUser
from django.db.models import Q
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class MessageCreateForm(forms.ModelForm):
    body = SummernoteTextField()

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'body' : SummernoteWidget()
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = StudentUser.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Advisors')).distinct()

    def clean(self):
        cleaned_data = super().clean()
        message = Message(
            recipient=cleaned_data.get('recipient'),
            subject=cleaned_data.get('subject'),
            body=cleaned_data.get('body')
        )

        return cleaned_data
    


class TeacherMessageCreateForm(forms.ModelForm):
    body = SummernoteTextField()

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'body' : SummernoteWidget()
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = StudentUser.objects.exclude(Q(groups__name='Teacher') | Q(groups__name='Advisors')).distinct()

    def clean(self):
        cleaned_data = super().clean()
        message = Message(
            recipient=cleaned_data.get('recipient'),
            subject=cleaned_data.get('subject'),
            body=cleaned_data.get('body')
        )

        return cleaned_data


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['subject', 'body']
        widgets = {
            'body': SummernoteWidget(),
        }