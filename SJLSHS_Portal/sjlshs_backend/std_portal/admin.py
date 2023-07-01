from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment
# Register your models here.

from .models import Post, Modules, Schedule, AdditionalResources



class PostAdmin(SummernoteModelAdmin):

    """
    PostAdmin class configures the admin interface for the Post model, and it is derived from 
    SummernoteModelAdmin which allows using the summernote rich text editor for the Body field. 
    It defines the save_model method to set the Author field to the full name of the user that created 
    the Post if it is a new instance. Also, it overrides the get_queryset method to limit the instances
    displayed in the list view according to the user's permissions.
    """

    list_display = ('id', 'Title', 'Author', 'Published')
    list_filter = ('Section',)
    search_fields = ('Title', 'Body')

    summernote_fields = ('Body',)

    exclude = ('Author',)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.Author = request.user.get_full_name()
        obj.save()


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(Author=request.user)
        
    def formfield_for_manytomany(self, db_field, request):
        formfield = super().formfield_for_manytomany(db_field, request)
        if not request.user.is_superuser:
            formfield.queryset = formfield.queryset.exclude(section='Universal')
        return formfield
            

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject',)
    list_filter = ('grade', 'subject',)
    search_fields = ('title', 'grade__name', 'subject__name',)
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview()

    thumbnail_preview.short_description = 'Thumbnail Preview'


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'schedule_file')
    list_filter = ('section',)
    search_fields = ('section__name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            advisory_section = request.user.teacheruser.advisory_section
            qs = qs.filter(section=advisory_section)
        return qs
    





admin.site.register(Post, PostAdmin)
admin.site.register(Modules, ModuleAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(AdditionalResources)
admin.site.unregister(Attachment)

