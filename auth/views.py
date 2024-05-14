from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from cards.serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


class Login(APIView):
    parser_classes: [JSONParser]
    permission_classes = []

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({
                "error": "Invalid Credentials",
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })


class Signup(APIView):
    parser_classes: [JSONParser]
    permission_classes = []

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.create_user(username, password=password)
        if user is None:
            return Response({
                "error": "Invalid Credentials",
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })


class Refresh(APIView):
    parser_classes: [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })
