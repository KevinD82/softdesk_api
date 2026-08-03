from django.conf import settings
from django.db import models


class Project(models.Model):
    TYPE_CHOICES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
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
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} -> {self.project.name}"


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Élevée'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Fonctionnalité'),
        ('TASK', 'Tâche'),
    ]

    STATUS_CHOICES = [
        ('TO_DO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('FINISHED', 'Terminé'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM'
    )
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='TO_DO'
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='issues'
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

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.issue.title}"