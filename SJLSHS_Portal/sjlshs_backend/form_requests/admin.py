from django.contrib import admin
from .models import Request, GoodMoral

# Register your models here.

admin.site.register(Request)


class GoodMoralAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'grade_level', 'lrn', 'purpose']
    list_filter = ['purpose']
    search_fields = ['full_name', 'lrn']
    readonly_fields = ['id']
    ordering = ('-id',)

    fieldsets = [
            ('Personal Information', {
                'fields': ['full_name', 'grade_level', 'lrn']
            }),
            ('Contact Information', {
                'fields': ['residence', 'contact', 'email']
            }),
            ('Other Details', {
                'fields': ['years_stayed', 'purpose', 'reasons', 'plans', 'transferring_school', 'transferring_strand', 'comments']
            }),
        ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(GoodMoral, GoodMoralAdmin)