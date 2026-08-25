from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.models import User
from authentication.serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """Vue d'inscription d'un utilisateur.

    Permet la création d'un compte via une requête HTTP POST.
    """

    # Queryset de base requis par DRF pour identifier le modèle associé
    queryset = User.objects.all()

    # Délégué au UserSerializer pour valider les données entrantes (champs RGPD, âge >= 15) et hacher le mot de passe
    serializer_class = UserSerializer

    # SÉCURITÉ & REST : Seule route d'inscription ouverte aux utilisateurs non authentifiés (AllowAny)
    permission_classes = (AllowAny,)