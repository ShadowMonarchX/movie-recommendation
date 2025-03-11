from ..cookies import *
from django.utils.timezone import now, make_aware
from ..models.user_models import *
from ..serializers.auth_serializers import *
from ..auth_requirement.validation import *
from ..auth_requirement.utils import send_generated_otp_to_email
from ..auth_requirement.social import register_social_user

from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.decorators import method_decorator


from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from django_ratelimit.decorators import ratelimit

#


from datetime import datetime
from multiprocessing import context

class RegisterView(APIView):
    permission_classes = [AllowAny]


    def post(self,request):
        validation_error = RegisterValidation(request)

        if validation_error:
            return validation_error
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "Invalid data provided.",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        if User.objects.filter(email=email).exists():
            return Response({
                "status": "failure",
                "message": "This email is already registered."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            user.is_verified = False
            user.save()

            if send_generated_otp_to_email(user.email, request):
                return Response({
                    "status": "success",
                    "message": "OTP sent to your email for verification.",
                    "data": {"email": user.email}
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "failure",
                    "message": "Failed to send OTP."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                "status": "failure",
                "message": "User creation failed.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp = request.data.get('otp')

        session_otp = request.session.get('otp')
        session_email = request.session.get('otp_email')
        otp_expiry = request.session.get('otp_expiry')

        if not otp or not session_otp or not session_email or not otp_expiry:
            return Response({
                "status": "failure",
                "message": "Invalid OTP or session expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_expiry_dt = datetime.strptime(otp_expiry, "%Y-%m-%d %H:%M:%S")
            otp_expiry_dt = make_aware(otp_expiry_dt)  # Ensure it's timezone-aware
        except ValueError:
            return Response({
                "status": "failure",
                "message": "Invalid session expiry format."
            }, status=status.HTTP_400_BAD_REQUEST)

        if now() > otp_expiry_dt:  # Compare timezone-aware datetime
            return Response({
                "status": "failure",
                "message": "OTP expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp != session_otp:
            return Response({
                "status": "failure",
                "message": "Invalid OTP."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=session_email)
        except User.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "User not found."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Clear session data
        request.session.pop('otp', None)
        request.session.pop('otp_email', None)
        request.session.pop('otp_expiry', None)
        request.session.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "status": "success",
            "message": "Email verified successfully.",
            "data": {
                "email": user.email,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        }, status=status.HTTP_200_OK)
        # response = JsonResponse({
        #     "status": "success",
        #     "message": "Email verified successfully.",
        #     "data": {
        #         "email": user.email,
        #     },
        #
        # })
        #
        # response = set_auth_cookie(response, user,request)
        # print(response)
        #
        # return response


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='user', rate='3/h', method='POST'))
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "status": "failure",
                "message": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "User with this email does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({
                "status": "failure",
                "message": "User is already verified."
            }, status=status.HTTP_400_BAD_REQUEST)


        if send_generated_otp_to_email(email, request):
            return Response({
                "status": "success",
                "message": "OTP resent to your email.",
                "data": {"email": email}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "failure",
                "message": "Failed to resend OTP."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response({
                "status": "failure",
                "message": "Invalid credentials."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            return Response({
                "status": "failure",
                "message": "Email not verified."
            }, status=status.HTTP_400_BAD_REQUEST)

        # refresh = RefreshToken.for_user(user)
        # return Response({
        #     "status": "success",
        #     "message": "Login successful.",
        #     "data": {
        #         "access_token": str(refresh.access_token),
        #         "refresh_token": str(refresh)
        #     }
        # }, status=status.HTTP_200_OK)
        response = JsonResponse({
            "status": "success",
            "message": "Login successful.",
            "data": {
                "email": user.email,
            }
        })

        response = set_auth_cookie(response, user)


        return response

class PasswordResetRequestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        validation_error = PasswordResetValidation(request)
        
        if validation_error:
            return validation_error
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try :
                user = User.objects.get(email=email)

                return Response({'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({'message': 'User with that email  not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64=None, token=None):
        if not uidb64 or not token:
            return Response({'message': 'Invalid request. Missing parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'success': True,
                'message': 'Credentials are valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)

        except (ValueError, User.DoesNotExist):
            return Response({'message': 'Token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_password = request.data.get('new_password')

        if not is_valid_password(new_password):
            return Response({
                'success': False,
                'message': "Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'message': "Password reset is successful."
        }, status=status.HTTP_200_OK)

class LogoutApiView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
 

class GoogleSignInView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        id_token = request.data.get("id_token") 

        if not access_token or not id_token:
            return Response(
                {"error": "Both access_token and id_token are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_data = register_social_user("google", access_token, id_token)  
        return Response(user_data, status=status.HTTP_200_OK)



# class GoogleAuthView(APIView):
#     def post(self, request):
#         return JsonResponse({"message": "Google Sign-in API working"})



# from django.conf import settings

# from rest_framework import serializers
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from requests.exceptions import HTTPError

# from social_django.utils import psa


# class SocialSerializer(serializers.Serializer):
#     access_token = serializers.CharField(
#         allow_blank=False,
#         trim_whitespace=True,
#     )


# @api_view(http_method_names=['POST'])
# @permission_classes([AllowAny])
# @psa()
# def exchange_token(request, backend):
#     serializer = SocialSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
        
#         try:
#             nfe = settings.NON_FIELD_ERRORS_KEY
#         except AttributeError:
#             nfe = 'non_field_errors'

#         try:
#             user = request.backend.do_auth(serializer.validated_data['access_token'])
#         except HTTPError as e:
#             return Response(
#                 {'errors': {
#                     'token': 'Invalid token',
#                     'detail': str(e),
#                 }},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if user:
#             if user.is_active:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key})
#             else:
    
#                 return Response(
#                     {'errors': {nfe: 'This user account is inactive'}},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         else:
#             return Response(
#                 {'errors': {nfe: "Authentication Failed"}},
#                 status=status.HTTP_400_BAD_REQUEST,
            # )

# class NetflixOauthSignInView(APIView):
#     serializer_class = NetflixLoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         access_token = serializer.validated_data['code']
#         user_data = register_social_user("netflix", access_token)

#         return Response(user_data, status=status.HTTP_200_OK)