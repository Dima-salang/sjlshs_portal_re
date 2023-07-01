"""sjlshs_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.admin import teacher_site
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import LoginView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailApp import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher/admin', teacher_site.urls),
    path('', include('std_portal.urls')),
    path('grades/', include('Grades_12.urls')),
    path('grades/', include('Grades_11.urls')),
    path('attendance/', include('attendance.urls')),
    path('irregular/', include('Irregular_Students.urls')),
    path('feedback/', include('feedback.urls')),
    path('org_apply/', include('org_applications.urls')),
    path('form_requests/', include('form_requests.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('/', include('django.contrib.auth.urls')),
    path('subjects/', include('subjects.urls')),
    path('calendar/', include('portal_calendar.urls')),
    path('messages/', include('messaging.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include(tf_urls)),
    path('login', LoginView.as_view(), name='login'),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('', include('wagtailApp.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('captcha/', include('captcha.urls')),
    

    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
