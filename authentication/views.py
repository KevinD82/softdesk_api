from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.models import User
from authentication.serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Vue d'inscription permettant à un nouvel utilisateur de créer un compte.
    Accès ouvert à tous (AllowAny).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)