from rest_framework import generics, response, status
from authentication.models.authentication_model import CustomUser
from authentication.serializers.register_serializer import RegisterSerializer


class AuthenticationVOne(generics.ListCreateAPIView) :

    def get(self, request, *args, **kwargs):
        qs = CustomUser.objects.all()
        registration_serializer_object = RegisterSerializer(qs, many=True)
        return response.Response(registration_serializer_object.data)


    def post(self, request, *args, **kwargs):
        registration_serializer_object = RegisterSerializer(data=request.data)
        if registration_serializer_object.is_valid():
            registration_serializer_object.save()
            return response.Response(registration_serializer_object.data, status=status.HTTP_201_CREATED)
        
        return response.Response(registration_serializer_object.errors, status=status.HTTP_400_BAD_REQUEST)