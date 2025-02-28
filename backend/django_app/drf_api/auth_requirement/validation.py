from curses.ascii import US


from rest_framework.response import Response
from rest_framework import status

import re


def RegisterValidation(request):
    user_data = request.data
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')

    if not email:
        return Response({
            "status": "failure",
            "message": "Email is required.",
            "error": "Missing email field."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not username:
        return Response({
            "status": "failure",
            "message": "Email is required.",
            "error": "Missing email field."
        }, status=status.HTTP_400_BAD_REQUEST)

    if not password:
        return Response({
            "status": "failure",
            "message": "Password is required.",
            "error": "Missing password field."
        }, status=status.HTTP_400_BAD_REQUEST)

    if not is_valid_email(email):
        return Response({
            "status": "failure",
            "message": "Invalid email format.",
            "error": "Invalid email."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not is_valid_data(username):
        return Response({
            "status": "failure",
            "message": "Invalid First Name or Last Name format.",
            "error": "Invalid First Name or Last Name."
        }, status=status.HTTP_400_BAD_REQUEST)
   

def PasswordResetValidation(request) :
    user_data = request.data
    email = user_data.get('email')

    if not email:
        return Response({
                "status": "failure",
                "message": "Email is required.",
                "error": "Missing email field."
        }, status=status.HTTP_400_BAD_REQUEST)
        
    if not is_valid_email(email):
        return Response({
            "status": "failure",
            "message": "Invalid email format.",
            "error": "Invalid email."
        }, status=status.HTTP_400_BAD_REQUEST)
    
def is_valid_email(email):

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    return re.match(email_regex, email) is not None

def is_valid_password(password):

    password_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?\d)(?=.*?[^\w\s]).{6,20}$"

    return re.match(password_regex, password) is not None

def is_valid_phone_number(phone_number):

    return phone_number.isdigit() and len(phone_number) == 10

def is_valid_data(username):

    return (6 <= len(username) <= 15)
