from django.db import models
from django.contrib.auth import get_user_model
from django_summernote.fields import SummernoteTextField, SummernoteTextFormField 




User = get_user_model()

class Message(models.Model):
        

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject

class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='replies_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='replies_received', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.subject




