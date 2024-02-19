"""
URL configuration for pythonApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from pythonApi import views
from rest_framework.urlpatterns import format_suffix_patterns


urlprefix = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(urlprefix + '/profile/<str:username>/', views.ProfileData),
    path(urlprefix + '/profiles', views.UserProfileList),
    path(urlprefix + '/profiles/<int:id>/', views.UserProfileDetail),
    path(urlprefix + '/profiles/delete', views.UserProfileList),
    path(urlprefix + '/media', views.MediaList),
    path(urlprefix + '/media/delete', views.MediaList),
    path(urlprefix + '/requests', views.RequestList),
    path(urlprefix + '/requests/delete', views.RequestDetail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
