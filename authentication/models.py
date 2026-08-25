from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour l'application SoftDesk.
    """

    birth_date = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def clean(self) -> None:
        super().clean()
        if self.birth_date:
            today = timezone.now().date()
            age = (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
            if age < 15:
                raise ValidationError(
                    "L'utilisateur doit être âgé d'au moins 15 ans."
                )

    def __str__(self) -> str:
        return self.username