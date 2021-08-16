from rest_framework import generics, response, status
from authentication.models import CustomUser
from authentication.serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from rest_framework.response import Response
from django.conf import settings
from authentication.tasks import send_email_task

class AuthenticationVOne(generics.ListCreateAPIView) :

    def get(self, request, *args, **kwargs):
        qs = CustomUser.objects.all()
        registration_serializer_object = RegisterSerializer(qs, many=True)
        return response.Response(registration_serializer_object.data)


    def post(self, request, *args, **kwargs):

        registration_serializer_object = RegisterSerializer(data=request.data)

        if registration_serializer_object.is_valid():

            registration_serializer_object.save()

            user_data = registration_serializer_object.data
            user = CustomUser.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.first_name + \
                ', Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            send_email_task(data)
            return response.Response(user_data, status=status.HTTP_201_CREATED)
        
        return response.Response(registration_serializer_object.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        return Response(login_serializer.data, status=status.HTTP_200_OK)