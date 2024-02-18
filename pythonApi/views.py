from django.http import JsonResponse
from .models import UserProfile
from .serializers import UserProfileSerializer
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
    return JsonResponse({
        'profile_pic_url': profile_pic_url,
        'user_name': user_name,
        'followers_count': followers_count,
        'follows_count': follows_count,
        'profile_url': profile_url,
        'media_count': media_count
    })

import requests
from bs4 import BeautifulSoup

def get_profile_info(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tags = soup.find_all('meta', attrs={'property': 'og:title'})
            if meta_tags:
                user_name = meta_tags[0]['content']
                user_name = user_name.split('(')[0].strip()  # Remove any additional text in the username
                profile_pic_meta = soup.find('meta', attrs={'property': 'og:image'})
                followers_count = soup.select_one('meta[property="og:description"][content]').get('content').split(' ')[0].replace(',','')
                follows_count = soup.select_one('meta[property="og:description"][content]').get('content').split(' ')[2].replace(',','')
                media_count = soup.select_one('meta[property="og:description"][content]').get('content').split(' ')[4].replace(',','')
                if profile_pic_meta:
                    profile_pic_url = profile_pic_meta['content']
                    profile_url = url
                    return [user_name, profile_pic_url, followers_count, follows_count, profile_url, media_count]
                else:
                    print("Profile picture URL not found.")
            else:
                print("Username not found.")
        else:
            print(f"Failed to fetch profile. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
