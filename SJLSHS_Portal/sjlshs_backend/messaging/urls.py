from django.urls import path
from .views import MessageInboxView, message_detail, MessageCreateView, MessageSentView, ReplyCreateView, TeacherMessagesView, TeacherMessagesCreateView, TeacherSentView
from django_otp.decorators import otp_required

urlpatterns = [
    path('inbox/', otp_required(MessageInboxView.as_view()), name='message-inbox'),
    path('<int:message_id>/', message_detail, name='message_detail'),
    path('write/', otp_required(MessageCreateView.as_view()), name='message-create'),
    path('sent/', otp_required(MessageSentView.as_view()), name='message-sent'),
    path('<int:message_id>/reply', otp_required(ReplyCreateView.as_view()), name='message-reply'),
    path('teacher/inbox', TeacherMessagesView.as_view(), name='teacher_message'),
    path('teacher/write', TeacherMessagesCreateView.as_view(), name='teacher_message_create'),
    path('teacher/sent', TeacherSentView.as_view(), name='teacher_sent'),
]