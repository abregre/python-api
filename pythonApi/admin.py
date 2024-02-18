from django.contrib import admin
from .models import UserProfile, Media, Request

admin.site.register(UserProfile)
admin.site.register(Media)
admin.site.register(Request)