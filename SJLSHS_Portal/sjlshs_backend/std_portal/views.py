from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from accounts.models import StudentUser, Enrolled_Students, StudentSection
from .models import Post, Modules, Schedule, AdditionalResources
from page_customization.models import CampusLifeImages
from portal_calendar.models import CalendarEvent
from .forms import ModuleFilterForm
from django.conf import settings
from django_otp.decorators import otp_required
from wagtail.models import Page
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from wagtailApp.models import ArticlePage
from django.core.paginator import Paginator
from django.core.cache import cache
from django_redis import get_redis_connection
# Create your views here.


redis_conn = get_redis_connection()


# ssg page objects
ssg_page = Page.objects.get(slug='supreme-student-government')



def home_page_view(request):
    """
    This function retrieves information about recent news, events, and announcements from the database
    and returns a rendered HTML template for the home page view.

    Args:
    request: HttpRequest object representing the current request.

    Returns:
    A rendered HTML template for the home page view with context containing recent events, news,
    and announcements.

    Raises:
    Page.DoesNotExist: If the 'supreme-student-government' page does not exist in the database.
    AttributeError: If any of the 'news', 'events', or 'announcements' child pages do not exist
    under the 'supreme-student-government' page.
    """

    news_page = ssg_page.get_children().get(slug='news')
    events_page = ssg_page.get_children().get(slug='events')
    announcements_page = ssg_page.get_children().get(slug='announcements')
    

    news_articles = cache.get('news_articles')
    events_posts = cache.get('events_posts')
    announcement_posts = cache.get('announcement_posts')

    if news_articles is None:
        news_articles = news_page.get_children().specific().live().order_by('-first_published_at')[:3]
        cache.set('news_articles', news_articles)
        redis_conn.expire('news_articles', 3600)
    if events_posts is None:
        events_posts = events_page.get_children().specific().live().order_by('-first_published_at')[:6]
        cache.set('events_posts', events_posts)
        redis_conn.expire('events_posts', 3600)
    if announcement_posts is None:
         announcement_posts = announcements_page.get_children().specific().live().order_by('-first_published_at')[:4]
         cache.set('announcement_posts', announcement_posts)
         redis_conn.expire('announcement_posts', 3600)

    
    campus_life_images = cache.get('campus_life_images')
    print(campus_life_images)
    if campus_life_images is None:
        campus_life_images = CampusLifeImages.objects.all().order_by('-date_posted')[:9]
        print(campus_life_images)
        cache.set('campus_life_images', campus_life_images)
        redis_conn.expire('campus_life_images', 3600)
    
    
    return render(request, 'home.html', {'recent_events': events_posts,
                                'recent_news': news_articles,
                                'recent_announcements': announcement_posts,
                                'campus_life_images' : campus_life_images})                               

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalHomeView(ListView):
    model = Post
    template_name = "portal-home.html"


@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalRedirectView(TemplateView):
    template_name = 'portal-redirect.html'

@otp_required
def update_users(request):
    auth_checks = 0
    queryset = Enrolled_Students.objects.all()
    user = settings.AUTH_USER_MODEL
    for student in queryset:
        if request.user.lrn == student.lrn:
            auth_checks += 50
        if request.user.last_name == student.last_name:
            auth_checks += 10
        if request.user.email == student.email:
            auth_checks += 10
        if auth_checks >= 70:
            request.user.section = student.section
            request.user.strand = student.strand

            request.user.save()
    return render(request, 'login-redirect.html', {})


@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalPersonalView(TemplateView):
    model = StudentUser
    template_name = 'portal-personal.html'
    
@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalAnnouncements(ListView):

    """
    A view for displaying a paginated list of Post objects filtered based on the currently logged-in user's section.

    Model: Post
    Template: portal-announcements.html

    Attributes:
    - paginate_by (int): Number of items to display per page

    Methods:
    - get_queryset(): Returns a queryset of Post objects filtered by the current user's section. 
      If the user is a superuser, returns all Post objects sorted by the 'Published' field.
    - get_context_data(): Adds a 'universal_section' object to the context dictionary for use in the template.

    Usage:
    The view expects a logged-in user object to be available in the request object.
    """


    model = Post
    template_name = "portal-announcements.html"
    paginate_by = 5 # Set the number of items to display per page
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Post.objects.all().prefetch_related('Section').order_by('-Published')
            print("superuser returned all objects in post queryset")
        else:
            queryset = Post.objects.prefetch_related('Section').filter(Q(Section=user.section)).order_by('-Published')
            print("user got posts related to their section")
        print("returned queryset")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        universal_section = StudentSection.objects.get(section='Universal')
        context['universal_posts'] = Post.objects.prefetch_related('Section').filter(Section=universal_section).order_by('-Published')[:2]
        print(context['universal_posts'])
        announcements_page = ssg_page.get_children().get(slug='announcements')
        context['recent_announcements'] = announcements_page.get_children().specific().live().order_by('-first_published_at')[:5]
        return context
    
    

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalSched(ListView):
    model = Schedule
    template_name = 'portal-sched.html'
    paginate_by = 7

    def get_queryset(self):
        qs =  super().get_queryset()
        qs = qs.filter(section=self.request.user.section)
        print(qs)
        return qs
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        universal_section = StudentSection.objects.get(section='Universal')
        events = CalendarEvent.objects.filter(Q(
            event_start_date__month=today.month,
            section=self.request.user.section
        ) | Q(event_start_date__month=today.month,
              section=universal_section)).order_by('-event_start_date')
        context['events'] = events
        return context

    def get_events(self, request):
        print("called get_events function")
        today = timezone.now().date()
        print(f"Timezone : {today}")
        universal_section = StudentSection.objects.get(section='Universal')
        events = CalendarEvent.objects.filter(Q(
            event_start_date__month=today.month,
            section=request.user.section
        ) | Q(event_start_date__month=today.month,
              section=universal_section))
        event_list = []
        for event in events:
            event_dict = {
                'title': event.event_title,
                'start': str(event.event_start_date),
                'end': str(event.event_end_date),
                'description': event.event_description,
                'level': str(event.event_level)
            }
            event_list.append(event_dict)
            print(event_dict)
        return JsonResponse(event_list, safe=False)

@user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists())
def search(request):
    """
    Renders a view that allows the user to search for modules by title, grade level, and/or subject.

    On a GET request, displays a form for the user to enter their search criteria.

    On a POST request, retrieves the user's search criteria from the request parameters and filters the modules based on
    the criteria. If no criteria are specified, all modules are displayed.

    The search results are displayed on the 'portal-modules-redirect.html' template, along with the search form and the
    search criteria entered by the user.

    Returns:
        A rendered view of the 'module-filter.html' template on a GET request, or a rendered view of the
        'portal-modules-redirect.html' template on a POST request.
    """

    form = ModuleFilterForm()

    # try to fetch results
    module_objs = cache.get('module_objs')
    print(f"cached: {module_objs}")
    additional_resources = cache.get('additional_resources')

    # If the cache is empty, fetch the data from the database and cache it
    if module_objs is None:
        module_objs = Modules.objects.select_related('grade', 'subject').all()
        print(module_objs)
        cache.set('module_objs', module_objs)
        redis_conn.expire('module_objs', 3600)  # expire the cache after 1 hour

    if additional_resources is None:
        additional_resources = AdditionalResources.objects.all()
        cache.set('additional_resources', additional_resources)
        redis_conn.expire('additional_resources', 3600)  # expire the cache after 1 hour

    modules = module_objs

    if request.method == 'POST':
        print("Got get request.")
        title = request.POST.get('title_search')
        print(f"Searching for {title}")
        grade_level = request.POST.get('grade_level')
        print(f"Searching for {grade_level}")
        subject = request.POST.get('subject')
        print(f"Searching for {subject}")

        if title or grade_level or subject:

            if title:
                modules = module_objs.filter(Q(title__icontains=title))
            if grade_level:
                modules = module_objs.filter(Q(grade=grade_level))
            if subject:
                modules = module_objs.filter(Q(subject=subject))
        
        context = {
            'modules': modules,
            'form' : form,
            'title' : title,
            'grade_level' : grade_level,
            'subject' : subject,
            'additional_resources' : additional_resources
        }

        return render(request, 'portal-modules-redirect.html', context)
    
    context = {
        'form' : form,
        'modules' : module_objs,
        'additional_resources' : additional_resources
    }
    return render(request, 'module-filter.html', context)


class PortalModuleRedirectG12(TemplateView):
    template_name = 'portal-modules-redirectG12.html'

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class PortalModules(ListView):
    template_name = 'portal-modules.html'


class PortalModulesUCSP(ListView):
    model = Modules
    template_name = 'portal-modules-ucsp.html'


class HomeOfferings(TemplateView):
    template_name = 'offerings.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class EnrollmentView(TemplateView):
    template_name = 'enrollment.html'


class FacultyView(TemplateView):
    template_name = 'faculty.html'


        



