from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Modèle représentant un projet dans l'application SoftDesk.

    Chaque projet possède un nom, une description, un type (ex: Backend, Frontend),
    un auteur (l'utilisateur qui l'a créé) et une date de création.
    """

    class TypeChoices(models.TextChoices):
        BACKEND = 'BACKEND', 'Back-end'
        FRONTEND = 'FRONTEND', 'Front-end'
        IOS = 'IOS', 'iOS'
        ANDROID = 'ANDROID', 'Android'

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects',
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Contributor(models.Model):
    """
    Table de liaison représentant l'appartenance d'un utilisateur à un projet.

    Permet d'accorder des droits d'accès/lecture/écriture aux membres enregistrés.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_user_project_contributor',
            ),
        )

    def __str__(self) -> str:
        username = getattr(self.user, 'username', 'Inconnu')
        project_name = getattr(self.project, 'name', 'Inconnu')
        return f"{username} -> {project_name}"


class Issue(models.Model):
    """
    Modèle représentant un ticket (problème, tâche ou fonctionnalité) rattaché à un projet.
    """

    class PriorityChoices(models.TextChoices):
        LOW = 'LOW', 'Faible'
        MEDIUM = 'MEDIUM', 'Moyenne'
        HIGH = 'HIGH', 'Élevée'

    class TagChoices(models.TextChoices):
        BUG = 'BUG', 'Bug'
        FEATURE = 'FEATURE', 'Fonctionnalité'
        TASK = 'TASK', 'Tâche'

    class StatusChoices(models.TextChoices):
        TO_DO = 'TO_DO', 'À faire'
        IN_PROGRESS = 'IN_PROGRESS', 'En cours'
        FINISHED = 'FINISHED', 'Terminé'

    title = models.CharField(max_length=128)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    tag = models.CharField(max_length=10, choices=TagChoices.choices)
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.TO_DO,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_issues',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    Modèle représentant un commentaire posté sur un ticket (Issue) spécifique.
    """

    description = models.TextField()
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        username = getattr(self.author, 'username', 'Inconnu')
        issue_title = getattr(self.issue, 'title', 'Inconnu')
        return f"Commentaire de {username} sur {issue_title}"