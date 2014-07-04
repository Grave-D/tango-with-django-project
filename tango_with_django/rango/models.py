from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # Liking UserProfile to User model
    user = models.OneToOneField(User)
    # Additional fields
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # Override __unicode__() method to return something useful
    def __unicode__(self):
        return self.user.username