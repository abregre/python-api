from django.http import JsonResponse
from .models import UserProfile, Media
from .serializers import UserProfileSerializer, MediaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def UserProfileList(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def UserProfileDetail(request, id):
    try:
        profile = UserProfile.objects.get(pk=id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ProfileData(request, username):

    [user_name, profile_pic_url, followers_count, follows_count, profile_url, media_count] = get_profile_info(username)
    media = get_media(username)

    return JsonResponse({
        'profile_pic_url': profile_pic_url,
        'user_name': user_name,
        'followers_count': followers_count,
        'follows_count': follows_count,
        'profile_url': profile_url,
        'media_count': media_count,
        'media': media
    })

import instaloader
from datetime import datetime, timedelta

def get_profile_info(username):
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        user_name = profile.full_name
        profile_pic_url = profile.profile_pic_url
        followers_count = profile.followers
        follows_count = profile.followees
        profile_url = f"https://www.instagram.com/{username}"
        media_count = profile.mediacount

        return [user_name, profile_pic_url, followers_count, follows_count, profile_url, media_count]

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def get_media(username):
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        posts = profile.get_posts()

        results = []
        maxPosts = 10
        for post in posts:
            url = post.shortcode
            thumbnail_url = post.url
            caption = post.caption
            likes = post.likes
            comments = post.comments
            date = post.date

            results.append({
                'url': url,
                'thumbnail_url': thumbnail_url,
                'caption': caption,
                'likes': likes,
                'comments': comments,
                'date': date
            })
            maxPosts -= 1
            if maxPosts == 0:
                break

        return results

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
