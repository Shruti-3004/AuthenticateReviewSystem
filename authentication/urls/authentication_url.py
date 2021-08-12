from authentication.serializers.register_serializer import RegisterSerializer
from django.urls import path, include
from authentication.views.authentication_view import AuthenticationVOne

urlpatterns = [
    path('v1/authenticate/', AuthenticationVOne.as_view()),
]