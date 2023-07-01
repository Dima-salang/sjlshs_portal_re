from django.urls import path
from .views import organization_application_view, OrganizationApplyView

urlpatterns = [
    path('apply-home/', organization_application_view, name='orgs-apply-home'),
    path('apply/', OrganizationApplyView.as_view(), name='orgs-apply-form'),

]