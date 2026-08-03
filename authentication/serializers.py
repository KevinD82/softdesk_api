from datetime import date

from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'birth_date',
            'can_be_contacted',
            'can_data_be_shared',
        ]

    def validate_birth_date(self, value):
        if value:
            today = date.today()
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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            birth_date=validated_data.get('birth_date'),
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
        )
        return user