from django.db import models
from django.contrib.postgres.fields import ArrayField

class UserProfile(models.Model):
    name= models.CharField(max_length=100, default='', blank=True, null=True)
    username = models.CharField(max_length=100)
    url = models.CharField(max_length=200, default='', blank=True, null=True)
    followersCount = models.IntegerField(default=0, blank=True, null=True)
    followsCount = models.IntegerField(default=0, blank=True, null=True)
    mediaCount = models.IntegerField(default=0, blank=True, null=True)
    profilePicUrl = models.CharField(max_length=200, default='', blank=True, null=True)
    def __str__(self):
        return self.username

class Media(models.Model):
    media_url = models.CharField(max_length=200, default='', blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, default='', blank=True, null=True)
    caption = models.CharField(max_length=500, default='', blank=True, null=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption