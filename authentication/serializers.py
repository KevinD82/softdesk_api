from typing import Any, ClassVar

from django.utils import timezone
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création et la gestion des utilisateurs.
    """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'birth_date',
            'can_be_contacted',
            'can_data_be_shared',
        )
        # Annotation ClassVar pour indiquer à Ruff que le dictionnaire est une constante de classe
        extra_kwargs: ClassVar[dict[str, Any]] = {'password': {'write_only': True}}

    def validate_birth_date(self, value):
        if value:
            today = timezone.now().date()
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
        return User.objects.create_user(**validated_data)