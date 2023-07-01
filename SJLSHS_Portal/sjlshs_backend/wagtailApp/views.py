from django.shortcuts import render
from wagtail.models import Page 
from datetime import datetime
from std_portal.forms import CareerCenterFilterForm
from django.core.paginator import Paginator

"""
This module contains views for a student portal website.

Functions:

home_page(request): Renders the homepage of the website, using the template 'home_page.html' and passing the context variable 'home_page', which contains the Page object for the homepage.

recent_links(request): Renders a page with recent news articles, using the template 'relevant_links.html' and passing the context variable 'recent_news_articles', which contains a list of the 10 most recent news articles published under the Supreme Student Government page.

career_center_view(request): Renders a page with career-related articles, using the template 'career-center.html' and passing the context variable 'career_articles', which contains a queryset of all live and specific children pages of the Career Center page. 
The function also filters the queryset based on the user input from the CareerCenterFilterForm, if it is valid. The context variable 'datetime_now' contains the current datetime object, and the context variable 'form' contains an instance of CareerCenterFilterForm.
"""

# Create your views here.
def home_page(request):
    home_page = Page.objects.get(slug='sjlshs-organizations')  # assuming 'home' is the slug for your home page
    return render(request, 'home_page.html', {'home_page': home_page})

def recent_links(request):
    ssg = Page.objects.get(slug='supreme-student-government')
    recent_news = ssg.get_children().get(slug='news')
    print(recent_news)
    recent_news_articles = recent_news.get_children().specific().live().order_by('-first_published_at')[:10]
    print(recent_news_articles)
    return render(request, "relevant_links.html", {'recent_news_articles': recent_news_articles})


def career_center_view(request):
    datetime_now = datetime.now()

    lac_pages = Page.objects.get(slug='litexian-achievers-club')
    print("got litexian pages")
    career_pages = lac_pages.get_children().filter(slug='career-center').first()
    print("got career pages")
    career_articles = career_pages.get_children().specific().live().order_by('-first_published_at')
    print("got articlces")

    reviewers_page = lac_pages.get_children().get(slug='reviewers')
    reviewer_articles = reviewers_page.get_children().specific().live().order_by('-first_published_at')

    scholarships_page = lac_pages.get_children().get(slug='scholarships')
    scholarship_articles = scholarships_page.get_children().specific().live().order_by('-first_published_at')

    form = CareerCenterFilterForm(request.GET)

    if form.is_valid():
        school_search = form.cleaned_data['school_search']
        if school_search:
            career_articles = career_articles.filter(title__icontains=school_search)
    
    context = {
        'career_articles' : career_articles,
        'datetime_now' : datetime_now,
        'form' : form,
        'reviewers' : reviewer_articles,
        'scholarships' : scholarship_articles
    }
    return render(request, 'career-center.html', context)


def faculty_staff_view(request):
    web_pages = Page.objects.get(slug='sjlshs-web-pages')
    faculty_staff = web_pages.get_children().get(slug='faculty-and-staff')
    print(web_pages)
    print(faculty_staff)

    context = {
        'faculty_staff' : faculty_staff
    }

    render(request, 'faculty.html', context)



def all_announcements_view(request):
    ssg_page = Page.objects.get(slug='supreme-student-government')
    announcements = ssg_page.get_children().get(slug='announcements')
    announcement_articles = announcements.get_children().specific().live().order_by('-first_published_at')

    paginator = Paginator(announcement_articles, 10)
    page_number = request.GET.get('get')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj
    }

    return render(request, 'all_announcements.html', context)