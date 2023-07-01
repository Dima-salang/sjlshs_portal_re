from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django_otp.decorators import otp_required
from django.urls import reverse_lazy
from messaging.models import Message, Reply
from django.views.generic import ListView, CreateView
from django.contrib.auth import get_user_model
from accounts.models import StudentUser
from django.db.models import Q
from django_summernote.fields import SummernoteTextFormField
from django_summernote.widgets import SummernoteWidget
from .forms import MessageCreateForm, ReplyForm, TeacherMessageCreateForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

User = get_user_model


@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class MessageInboxView(ListView):
    model = Message
    template_name = 'messaging/message_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(recipient=self.request.user) 
        print('Recipient:', self.request.user.id)
        for msg in qs:
            print('Message recipient:', msg.recipient.id)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toast_shown'] = self.request.COOKIES.get('toast_shown', False)
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.COOKIES.get('toast_shown', False):
            response.set_cookie('toast_shown', True)
        return response


@otp_required
@user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists())
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    print(message)
    message.read_at = timezone.now()
    message.save()

    replies = message.replies.all()

    if request.method == 'POST':
        print("called POST method")
        form = ReplyForm(request.POST)
        print(form)
        if form.is_valid():
            reply = form.save(commit=False)
            print(reply)
            reply.message = message
            print(reply.message)
            reply.sender = request.user
            reply.recipient = message.sender if message.recipient == request.user else message.recipient
            reply.save()
            
            return redirect('message_detail', message_id=message_id)
    else:
        form = ReplyForm()
        print(f"initial form {form}")
    return render(request, 'messaging/message_detail.html', {'message': message,
                                                             'form' : form,
                                                             'replies' : replies})

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class MessageCreateView(CreateView):
    form_class = MessageCreateForm
    template_name = 'messaging/message_create.html'
    success_url = reverse_lazy('message-inbox')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    
@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class MessageSentView(ListView):
    model = Message
    template_name = 'messaging/message_sent.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(sender=self.request.user)
        return qs


@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class ReplyCreateView(CreateView):
    model = Reply
    fields = ['subject', 'body']
    template_name = 'messaging/reply_create.html'


class TeacherMessagesView(ListView):
    model = Message
    template_name = 'messaging/teacher_message.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(recipient=self.request.user) 
        print('Recipient:', self.request.user.id)
        for msg in qs:
            print('Message recipient:', msg.recipient.id)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toast_shown'] = self.request.COOKIES.get('toast_shown', False)
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.COOKIES.get('toast_shown', False):
            response.set_cookie('toast_shown', True)
        return response
    

class TeacherMessagesCreateView(CreateView):
    form_class = TeacherMessageCreateForm
    template_name = 'messaging/teacher_message_create.html'
    success_url = reverse_lazy('teacher_message')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
    

class TeacherSentView(ListView):
    model = Message
    template_name = 'messaging/teacher_message_sent.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(sender=self.request.user)
        return qs
    
