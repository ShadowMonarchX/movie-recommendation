from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.http import HttpResponse


User = get_user_model()

def set_auth_cookie(response, user, request):
    refresh = RefreshToken.for_user(user)
    
    response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
    response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')

    cookie_value = request.COOKIES.get('my_cookie', 'default_value')

    if 'access_token' in request.COOKIES:
        print("Access token found in request cookies:", request.COOKIES['access_token'])
        return HttpResponse(f'The value of my_cookie is {cookie_value}')
    else:
        print("Access token NOT found in request cookies.")
    return response 