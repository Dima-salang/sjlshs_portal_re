from django.db import models

# Create your models here.
class CampusLifeImages(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='media/page_customization')
    date_posted = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    