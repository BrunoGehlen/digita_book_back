from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CredentialSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, CredentialSerializer
from .models import Profile


class AccountCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
            )

            Profile.objects.create(user=user, email=request.data["email"])

        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




class LoginView(APIView):
    def post(self, request):
        serializer = CredentialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
