from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    followers = models.IntegerField()
    following = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + str(self.created_at)