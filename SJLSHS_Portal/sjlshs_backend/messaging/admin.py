from typing import Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .models import Message, Reply
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse

# Register your models here.

class MessageAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

    list_display = ('id', 'sender', 'recipient', 'subject', 'created_at', 'read_at')
    list_filter = ('sender', 'recipient', 'created_at', 'read_at')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'body')

    exclude = ('sender',)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user.get_full_name()
        obj.save()


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(sender=request.user)
        
    def changelist_view(self, request: HttpRequest, extra_context: Dict[str, str] | None = ...) -> TemplateResponse:
        redirect_url = reverse('teacher_message')
        return HttpResponseRedirect(redirect_url)



admin.site.register(Message, MessageAdmin)
admin.site.register(Reply)