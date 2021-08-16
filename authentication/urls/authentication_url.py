from authentication.serializers.register_serializer import RegisterSerializer
from django.urls import path, include
from authentication.views.authentication_view import AuthenticationVOne, VerifyEmail, LoginAPIView

urlpatterns = [
    path('v1/authenticate/', AuthenticationVOne.as_view()),
    path('v1/authenticate/email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('v1/authenticate/login/', LoginAPIView.as_view(), name='login'),
]