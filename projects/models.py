import uuid

from django.conf import settings
from django.db import models


class Project(models.Model):
    """Modèle représentant un projet dans l'application SoftDesk.

    Regroupe les tickets d'incidents (Issues) et les contributeurs associés.
    """

    class TypeChoices(models.TextChoices):
        """Types de projets supportés par la plateforme."""

        BACKEND = "BACKEND", "Back-end"
        FRONTEND = "FRONTEND", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField(max_length=128)  # Nom du projet
    description = models.TextField(blank=True)  # Description facultative
    type = models.CharField(max_length=10, choices=TypeChoices.choices)  

    # RGPD / CASCADE : Si le compte utilisateur de l'auteur est supprimé,
    # le projet est supprimé en cascade pour respecter le droit à l'oubli.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)  # Horodatage automatique

    class Meta:
        ordering = ("-created_time",)  # Tri par défaut du plus récent au plus ancien

    def __str__(self) -> str:
        return self.name  


class Contributor(models.Model):
    """Table d'association représentant l'appartenance d'un utilisateur à un projet.

    Indispensable pour la vérification des permissions (seuls les contributeurs
    peuvent accéder aux ressources d'un projet).
    """

    # Lien vers l'utilisateur membre (suppression en cascade pour RGPD)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    # Lien vers le projet associé
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    created_time = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ("-created_time",)  
        constraints = (
            # SÉCURITÉ / INTEGRITÉ : Empêche l'ajout en double d'un même utilisateur sur un projet
            models.UniqueConstraint(
                fields=["user", "project"],
                name="unique_user_project_contributor",
            ),
        )

    def __str__(self) -> str:
        username = getattr(self.user, "username", "Inconnu")  
        project_name = getattr(self.project, "name", "Inconnu")  
        return f"{username} -> {project_name}"  


class Issue(models.Model):
    """Modèle représentant un ticket (problème, tâche ou fonctionnalité) rattaché à un projet."""

    class PriorityChoices(models.TextChoices):
        """Niveaux de priorité possibles."""

        LOW = "LOW", "Faible"
        MEDIUM = "MEDIUM", "Moyenne"
        HIGH = "HIGH", "Élevée"

    class TagChoices(models.TextChoices):
        """Balises de classification du ticket."""

        BUG = "BUG", "Bug"
        FEATURE = "FEATURE", "Fonctionnalité"
        TASK = "TASK", "Tâche"

    class StatusChoices(models.TextChoices):
        """États d'avancement du ticket."""

        TO_DO = "TO_DO", "À faire"
        IN_PROGRESS = "IN_PROGRESS", "En cours"
        FINISHED = "FINISHED", "Terminé"

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

    # Relation vers le projet parent
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    # Auteur du ticket (suppression en cascade RGPD)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )
    # Utilisateur assigné au traitement du ticket.
    # SET_NULL : Si le compte de l'assigné est supprimé, le ticket reste conservé mais l'assignation passe à Null.
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ("-created_time",)  

    def __str__(self) -> str:
        return self.title  


class Comment(models.Model):
    """Modèle représentant un commentaire posté sur un ticket (Issue) spécifique."""

    # SÉCURITÉ / BONNES PRATIQUES : Emploi d'un identifiant unique universel (UUID)
    # comme clé primaire pour éviter l'énumération séquentielle des identifiants (OWASP).
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField()  # Contenu du commentaire

    # Lien vers le ticket parent
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    # Auteur du commentaire (suppression en cascade RGPD)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ("-created_time",)  

    def __str__(self) -> str:
        username = getattr(self.author, "username", "Inconnu")  
        issue_title = getattr(self.issue, "title", "Inconnu")  
        return f"Commentaire de {username} sur {issue_title}"  