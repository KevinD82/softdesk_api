from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Modèle utilisateur personnalisé pour l'application SoftDesk.

    Étend AbstractUser pour ajouter les champs requis par le RGPD.
    """

    # Champ requis pour la vérification de l'âge légal (RGPD - consentement > 15 ans)
    birth_date = models.DateField(null=True, blank=True)

    # Consentement explicite : accord de l'utilisateur pour être contacté
    can_be_contacted = models.BooleanField(default=False)

    # Consentement explicite : accord de l'utilisateur pour le partage de ses données
    can_data_be_shared = models.BooleanField(default=False)

    def clean(self) -> None:
        """Validation au niveau du modèle.

        S'assure que l'utilisateur a au moins 15 ans pour respecter les exigences
        du RGPD concernant le consentement des mineurs.
        """
        super().clean()
        if self.birth_date:
            today = timezone.now().date()
            # Calcul précis de l'âge en prenant en compte le mois et le jour de naissance
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
        """Représentation lisible du modèle sous forme de chaîne (ex: dans l'admin Django)."""
        return self.username