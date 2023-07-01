from django.http import HttpResponse
from django.shortcuts import render
from .models import Organization, OrganizationApplication
from django.views.generic import FormView
from .forms import OrganizationApplicationForm
from django.utils import timezone
from django.contrib import messages
from wagtail.models import Page

# Create your views here.
def organization_application_view(request):
    organizations_page = Page.objects.get(slug='sjlshs-organizations')
    organizations = organizations_page.get_children().specific()

    context = {
        'organizations' : organizations
    }
    
    return render(request, 'org_apply/org_applications_home.html', context)


class OrganizationApplyView(FormView):
    template_name = 'org_apply/apply.html'
    form_class = OrganizationApplicationForm
    success_url = 'orgs-apply-home'
    

    def form_valid(self, form):
        org_form = form.save(commit=False)
        org_form.applicant = self.request.user
        org_form.date_submitted = timezone.now()

        if OrganizationApplication.objects.filter(applicant=org_form.applicant).exists():
            messages.error(self.request, "You can only apply for an organization once.")
            return self.form_invalid(form)
        else:
            org_form.save()
            messages.success(self.request, f"Application form submitted successfully!")
            return super().form_valid(form)

