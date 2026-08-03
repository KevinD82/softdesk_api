from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from authentication.models import User
from authentication.serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]