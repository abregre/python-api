from django.db import models

class UserProfile(models.Model):
    user_name= models.CharField(max_length=100, default='', blank=True, null=True)
    username = models.CharField(max_length=100, default='', blank=True, null=True)
    biography = models.CharField(max_length=500, default='', blank=True, null=True)
    url = models.CharField(max_length=200, default='', blank=True, null=True)
    followers_count = models.IntegerField(default=0, blank=True, null=True)
    follows_count = models.IntegerField(default=0, blank=True, null=True)
    media_count = models.IntegerField(default=0, blank=True, null=True)
    profile_pic_url = models.CharField(max_length=500, default='', blank=True, null=True)
    def __str__(self):
        return self.user_name

class Media(models.Model):
    media_url = models.CharField(max_length=500, default='', blank=True, null=True)
    thumbnail_url = models.CharField(max_length=500, default='', blank=True, null=True)
    caption = models.CharField(max_length=500, default='', blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    comments = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

class Request(models.Model):
    username = models.CharField(max_length=100, default='', blank=True, null=True)
    request_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    def __str__(self):
        return self.username