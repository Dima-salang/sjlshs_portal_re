from django.contrib import admin

# Register your models here.

from django.contrib import admin
from wagtail.documents import models as wagtailDocModel
from wagtail.images import models as wagtailImgModel
from taggit.models import Tag

admin.site.unregister(wagtailDocModel.Document)
admin.site.unregister(wagtailImgModel.Image)
admin.site.unregister(Tag)