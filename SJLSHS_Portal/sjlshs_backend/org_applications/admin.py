from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Organization, OrganizationApplication
from django.db.models import Q
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'adviser', 'president')
    search_fields = ('organization_name', 'adviser__username', 'president__username')
    list_filter = ('adviser', 'president')
    readonly_fields = ('organization_wagtail_url',)

class OrganizationApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'organization', 'date_submitted')
    search_fields = ('applicant__username', 'organization__organization_name')
    list_filter = ('organization', 'date_submitted')
    ordering = ('-date_submitted',)


    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return qs
        else:
            qs = qs.filter(Q(organization__adviser=user) | Q(organization__president=user))
        return qs

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationApplication, OrganizationApplicationAdmin)