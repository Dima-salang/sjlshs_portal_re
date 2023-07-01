from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, TabbedInterface, MultiFieldPanel, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.search import index
from modelcluster.models import ClusterableModel


"""
Module containing Django models for a student organization website.

Classes:

ArticlePage: Represents a page for an article, with fields for body, date, and feed image, and methods for retrieving recent news, events, and announcements.
OrgHomePage: Represents the homepage for a student organization, with fields for body and feed image.
IndexPage: Represents an index page, with fields for body, date, and feed image.
ArticleIndexPage: Represents an index page for articles, with fields for body and a method for retrieving the latest articles.
ArticleIndexPageLatestArticles: An orderable class for adding latest articles to an ArticleIndexPage.
CareerInformationArticle: Represents a page for career information, with fields for school image, description, and enrollment period.
"""

class ArticlePage(Page):
    body = RichTextField(blank=True)
    date = models.DateField("Post date", null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_description = models.CharField(max_length=255, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('feed_image'),
        FieldPanel('body', classname="full"),
        FieldPanel('short_description'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])

    def get_recent_news(self):
        ssg = Page.objects.get(slug='supreme-student-government')
        recent_news = ssg.get_children().get(slug='news')
        print(recent_news)
        recent_news_articles = recent_news.get_children().specific().live().order_by('-first_published_at')[:10]
        print(recent_news_articles)
        return recent_news_articles
    
    def get_recent_events(self):
        ssg = Page.objects.get(slug='supreme-student-government')
        recent_events = ssg.get_children().get(slug='events')
        print(recent_events)
        recent_events_articles = recent_events.get_children().specific().live().order_by('-first_published_at')[:5]
        print(recent_events_articles)
        return recent_events_articles
    
    def get_recent_announcements(self):
        ssg = Page.objects.get(slug='supreme-student-government')
        recent_announcements = ssg.get_children().get(slug='announcements')
        print(recent_announcements)
        recent_announcement_articles = recent_announcements.get_children().specific().live().order_by('-first_published_at')[:5]
        print(recent_announcement_articles)
        return recent_announcement_articles



class OrgHomePage(Page):
    short_description = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", null=True, blank=True, auto_now=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('feed_image'),
        FieldPanel('short_description'),
    ]

    def get_announcements(self):
        announcements = self.get_children().get(slug='announcements')
        print(announcements)
        recent_announcement_articles = announcements.get_children().specific().live().order_by('-first_published_at')[:5]

        return recent_announcement_articles

    def get_news(self):
        news = self.get_children().get(slug='news')
        recent_news_articles = news.get_children().specific().live().order_by('-first_published_at')[:6]
        return recent_news_articles
    
    def get_events(self):
        events = self.get_children().get(slug='events')
        recent_events_articles = events.get_children().specific().live().order_by('-first_published_at')[:6]
        return recent_events_articles
    


class IndexPage(Page):
    body = RichTextField(blank=True)
    date = models.DateField("Post date", null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('feed_image')
    ]




class ArticleIndexPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        InlinePanel("latest_articles", label="Latest Articles"),
    ]


class ArticleIndexPageLatestArticles(Orderable):
    page = ParentalKey(ArticleIndexPage, on_delete=models.CASCADE, related_name="latest_articles")
    article = models.ForeignKey(ArticlePage, on_delete=models.CASCADE, related_name="+", blank=True, null=True)

    panels = [
        FieldPanel("article"),
    ]


class CareerInformationArticle(Page):
    School_Image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    School_Description = RichTextField(blank=True)
    enrollment_period_start = models.DateField(null=True, blank=True)
    enrollment_period_end = models.DateField(null=True, blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('School_Description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('School_Image'),
        FieldPanel('School_Description', classname="full"),
        MultiFieldPanel([
            FieldPanel('enrollment_period_start'),
            FieldPanel('enrollment_period_end'),
    ],'Enrollment Period'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])


class StaffMember(ClusterableModel):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bio = RichTextField(blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('bio'),
        FieldPanel('photo'),
    ]

    def __str__(self):
        return self.name


class FacultyStaffPage(Page):
    template = "faculty_staff.html"
    max_count = 1
    subpage_types = []
    
    # This will allow us to add and remove staff members to this page
    content_panels = Page.content_panels + [
        InlinePanel('staff_members', label="Staff Members"),
    ]
    
    def get_staff_members(self):
        return self.staff_members.all()
        

class FacultyStaffPageStaffMemberRelationship(models.Model):
    page = ParentalKey(FacultyStaffPage, related_name='staff_members')
    staff_member = models.ForeignKey(
        StaffMember, 
        on_delete=models.CASCADE,
        related_name='+'
    )
    panels = [
        FieldPanel('staff_member')
    ]