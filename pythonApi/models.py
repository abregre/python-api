from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    followersCount = models.IntegerField()
    followsCount = models.IntegerField()
    profilePicUrl = models.CharField(max_length=200)

    def __str__(self):
        return self.username