from django.http import JsonResponse
from .models import UserProfile, Request, Media
from .serializers import UserProfileSerializer, RequestSerializer, MediaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
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

    elif request.method == 'DELETE':
        UserProfile.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
def RequestList(request):
    if request.method == 'GET':
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def RequestDetail(request):
    if(request.method == 'DELETE'):
        Request.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def MediaList(request):
    if request.method == 'GET':
        media = Media.objects.all()
        serializer = MediaSerializer(media, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def MediaDetail(request):
    if(request.method == 'DELETE'):
        Media.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ProfileData(request, username):

    try:
        dbRequest = Request.objects.filter(username=username, success=True).latest('request_time')

        if Request.objects.filter(username=username,success=True).count() > 1:
            Request.objects.filter(username=username, success=True).exclude(id=dbRequest.id).delete()
        elif Request.objects.filter(username=username,success=False):
            Request.objects.filter(username=username, success=False).delete()
    except Request.DoesNotExist:
        dbRequest = None

    if dbRequest:
        if dbRequest.request_time > (timezone.now() - timedelta(days=1)):
            user_name, biography, profile_pic_url, followers_count, follows_count, profile_url, media_count = get_profile_info_db(username)
            media = get_media_db(username)

            return JsonResponse({
                'profile_pic_url': profile_pic_url,
                'biography': biography,
                'user_name': user_name,
                'username': username,
                'followers_count': followers_count,
                'follows_count': follows_count,
                'profile_url': profile_url,
                'media_count': media_count,
                'media': media
            })
    else:

        user_name, biography, profile_pic_url, followers_count, follows_count, profile_url, media_count = fetch_profile_info_ext(username)
        media = get_media_ext(username)

        is_success = user_name is not None and biography is not None and profile_pic_url is not None and followers_count is not None and follows_count is not None and profile_url is not None and media_count is not None and media is not None

        if not is_success:
            return JsonResponse({
                'error': 'Profile not found'
            })

        requestSerializer = RequestSerializer(data={'username': username, 'success': True})

        if requestSerializer.is_valid():
            requestSerializer.save()


        profileSerializer = UserProfileSerializer(data={
            'user_name': user_name,
            'biography': biography,
            'profile_pic_url': profile_pic_url,
            'followers_count': followers_count,
            'follows_count': follows_count,
            'url': profile_url,
            'media_count': media_count,
            'username': username
        })
        dbProfile = UserProfile.objects.filter(username=username)

        if profileSerializer.is_valid() and not dbProfile:
            profileSerializer.save()


        userProfile = UserProfile.objects.get(username=username)
        for m in media:
            m['userProfile'] = userProfile.id

        mediaSerializer = MediaSerializer(data=media, many=True)
        if mediaSerializer.is_valid():
            mediaSerializer.save()
        elif mediaSerializer.errors:
            print(mediaSerializer.errors, 'mediaSerializer.errors')



    return JsonResponse({
        'profile_pic_url': profile_pic_url,
        'biography': biography,
        'user_name': user_name,
        'followers_count': followers_count,
        'follows_count': follows_count,
        'profile_url': profile_url,
        'media_count': media_count,
        'media': media
    })



import instaloader
from datetime import timedelta
from django.utils import timezone

def fetch_profile_info_ext(username):

    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        user_name = profile.full_name
        biography = profile.biography
        profile_pic_url = profile.profile_pic_url
        followers_count = profile.followers
        follows_count = profile.followees
        profile_url = f"https://www.instagram.com/{username}"
        media_count = profile.mediacount


        return user_name, biography, profile_pic_url, followers_count, follows_count, profile_url, media_count

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
        return [None, None, None, None, None, None, None]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [None, None, None, None, None, None, None]

def get_profile_info_db(username):
    try:
        profile = UserProfile.objects.get(username=username)
        user_name = profile.user_name
        biography = profile.biography
        profile_pic_url = profile.profile_pic_url
        followers_count = profile.followers_count
        follows_count = profile.follows_count
        profile_url = profile.url
        media_count = profile.media_count

        return user_name, biography, profile_pic_url, followers_count, follows_count, profile_url, media_count

    except UserProfile.DoesNotExist:
        return [None, None, None, None, None, None, None]

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [None, None, None, None, None, None, None]


def get_media_ext(username):
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
                'media_url': 'https://www.instagram.com/p/' + url + '/',
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
        return [None, None, None, None, None, None]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [None, None, None, None, None, None]


def get_media_db(username):
    try:
        profile = UserProfile.objects.get(username=username)
        media = Media.objects.filter(userProfile=profile)

        results = []
        for post in media:
            results.append({
                'media_url': post.media_url,
                'thumbnail_url': post.thumbnail_url,
                'caption': post.caption,
                'likes': post.likes,
                'comments': post.comments,
                'date': post.date
            })

        return results

    except UserProfile.DoesNotExist:
        return [None, None, None, None, None, None]

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [None, None, None, None, None, None]