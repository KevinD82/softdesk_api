from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.birth_date:
            today = date.today()
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
                    "L'utilisateur doit avoir au moins 15 ans."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)