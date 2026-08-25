from typing import Any, ClassVar

from django.utils import timezone
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création et la gestion des utilisateurs.

    Gère la transformation des données JSON et la validation métier lors de
    l'inscription.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "birth_date",
            "can_be_contacted",
            "can_data_be_shared",
        )
        # SÉCURITÉ OWASP : Le mot de passe est en "write_only".
        # Il peut être envoyé lors de la création, mais ne sera JAMAIS renvoyé dans les réponses API.
        extra_kwargs: ClassVar[dict[str, Any]] = {
            "password": {"write_only": True}
        }

    def validate_birth_date(self, value):
        """Validation au niveau du serializer (API).

        CONFORMITÉ RGPD : Vérifie que l'utilisateur a au moins 15 ans lors du
        traitement de la requête POST/PUT, renvoyant une erreur HTTP 400 Bad
        Request si la condition n'est pas remplie.
        """
        if value:
            today = timezone.now().date()
            # Calcul dynamique et précis de l'âge en années
            age = (
                today.year
                - value.year
                - ((today.month, today.day) < (value.month, value.day))
            )
            if age < 15:
                raise serializers.ValidationError(
                    "L'utilisateur doit avoir au moins 15 ans."
                )
        return value

    def create(self, validated_data):
        """SÉCURITÉ OWASP / BONNES PRATIQUES DJANGO :

        Utilise `create_user` au lieu de `create` standard afin d'assurer
        le hachage sécurisé du mot de passe (via PBKDF2/Bcrypt) avant la
        sauvegarde en base de données.
        """
        return User.objects.create_user(**validated_data)