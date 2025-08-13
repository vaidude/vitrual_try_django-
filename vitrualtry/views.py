from django.shortcuts import render,redirect,HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("HELLO")

from .utils import search_dresses  # assuming search_dresses is in utils.py

def dress_search(request):
    if request.method == 'POST':
        style = request.POST.get('style')
        gender = request.POST.get('gender')
        api_key = settings.SEPAPI_KEY
        
        # Pass gender to search_dresses
        dresses = search_dresses(style, api_key, gender)
        
        return render(request, 'dress_results.html', {'dresses': dresses})
    
    return render(request, 'dress_search.html')

# tryon/views.py
import http.client
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from django.conf import settings
# tryon/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import os
from django.conf import settings

# def try_on_page(request):
#     dress_url = request.GET.get('dress_url')
    
#     if request.method == 'POST':
#         avatar_url = request.POST.get('avatar_url')
        
#         if not dress_url or not avatar_url:
#             return JsonResponse({'error': 'Both dress URL and avatar URL are required.'}, status=400)

#         params = {
#             'clothing_image_url': dress_url,
#             'avatar_image_url': avatar_url
#         }
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'X-RapidAPI-Key': settings.RAPID_API_KEY,
#             'X-RapidAPI-Host': 'texel-virtual-try-on.p.rapidapi.com'
#         }

#         try:
#             response = requests.post(
#                 'https://texel-virtual-try-on.p.rapidapi.com/try-on-url',
#                 headers=headers,
#                 data=params
#             )

#             # Check Content-Type to determine response format
#             content_type = response.headers.get('Content-Type')
#             if content_type == 'image/jpeg':
#                 # Save the image result in media directory
#                 result_dir = os.path.join(settings.BASE_DIR, 'media', 'tryon')
#                 os.makedirs(result_dir, exist_ok=True)
#                 result_path = os.path.join(result_dir, 'result.jpg')

#                 with open(result_path, 'wb') as output_file:
#                     output_file.write(response.content)
                
#                 # Use relative URL for media file
#                 result_image_url = f'/media/tryon/result.jpg'

#                 # Return the relative URL of the saved image
#                 return render(request, 'try_on_result.html', {'result_image': result_image_url})

#             elif content_type == 'application/json':
#                 # Handle JSON error response
#                 response_json = response.json()
#                 print(response_json)
#                 return JsonResponse({'error': response_json.get('error', 'Unknown error occurred')}, status=500)

#             else:
#                 response_json = response.json()
#                 print(response_json)
#                 # Handle unexpected content types
#                 return JsonResponse({'error': 'Unexpected response format received.'}, status=500)
        
#         except requests.exceptions.RequestException as error:
#             return JsonResponse({'error': f'Network error occurred: {str(error)}'}, status=500)

#     return render(request, 'try_on_page.html', {'dress_url': dress_url})

import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET,
)

def upload_to_cloudinary(image_file):
    # Perform transformation (resize to 1280x1920 and convert to .jpg)
    response = cloudinary.uploader.upload(
        image_file,
        transformation=[
            {'width': 1280, 'height': 1920, 'crop': 'fill', 'format': 'jpg'}
        ]
    )
    print("Upload", response)
    return response['secure_url']

def try_on_page(request):
    dress_url = request.GET.get('dress_url')
    print('hi',dress_url)
    if request.method == 'POST':
        avatar_image = request.FILES.get('avatar_image')
        print('hello',avatar_image)
        
        if not dress_url or not avatar_image:
            return JsonResponse({'error': 'Both dress URL and avatar image are required.'}, status=400)

        try:
            avatar_url = upload_to_cloudinary(avatar_image)
            print('Uploading', avatar_url)
            
            # Proceed with the rest of your logic here
            params = {
                'clothing_image_url': dress_url,
                'avatar_image_url': avatar_url
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-RapidAPI-Key': settings.RAPID_API_KEY,
                'X-RapidAPI-Host': 'texel-virtual-try-on.p.rapidapi.com'
            }

            # Make the API request as before
            response = requests.post(
                'https://texel-virtual-try-on.p.rapidapi.com/try-on-url',
                headers=headers,
                data=params
            )
            
            content_type = response.headers.get('Content-Type')
            if content_type == 'image/jpeg':
                # Save the image result in media directory
                result_dir = os.path.join(settings.BASE_DIR, 'media', 'tryon')
                os.makedirs(result_dir, exist_ok=True)
                result_path = os.path.join(result_dir, 'result.jpg')

                with open(result_path, 'wb') as output_file:
                    output_file.write(response.content)
                
                # Use relative URL for media file
                result_image_url = f'/media/tryon/result.jpg'

                # Return the relative URL of the saved image
                return render(request, 'try_on_result.html', {'result_image': result_image_url})

            elif content_type == 'application/json':
                # Handle JSON error response
                response_json = response.json()
                print(response_json)
                return JsonResponse({'error': response_json.get('error', 'Unknown error occurred')}, status=500)

            else:
                response_json = response.json()
                print(response_json)
                # Handle unexpected content types
                return JsonResponse({'error': 'Unexpected response format received.'}, status=500)
        
        except requests.exceptions.RequestException as error:
            return JsonResponse({'error': f'Network error occurred: {str(error)}'}, status=500)

    return render(request, 'try_on_page.html', {'dress_url': dress_url})


