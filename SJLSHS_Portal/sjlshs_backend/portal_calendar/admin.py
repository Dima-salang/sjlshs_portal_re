from django.contrib import admin
from .models import CalendarEvent, EventLevel
from django.contrib.admin import ModelAdmin

# Register your models here.

class EventAdmin(ModelAdmin):

    list_display = ('event_title', 'author','event_start_date', 'event_end_date')
    list_filter = ('event_level',)
    search_fields = ('event_title', 'author', 'event_description')

    fieldsets = (
        (None, {'fields': ('event_title', 'event_description')}),
        ('Date and time', {'fields': ('event_start_date', 'event_end_date')}),
        ('Section', {'fields': ('section',)}),
        ('Level', {'fields': ('event_level',)}),
    )


    exclude = ('author',)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.get_full_name()
        obj.save()


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)
        
    def formfield_for_manytomany(self, db_field, request):
        formfield = super().formfield_for_manytomany(db_field, request)
        if not request.user.is_superuser:
            formfield.queryset = formfield.queryset.exclude(section='Universal')
        return formfield
            


admin.site.register(CalendarEvent, EventAdmin)