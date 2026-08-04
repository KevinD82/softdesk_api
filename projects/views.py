from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from projects.models import Comment, Contributor, Issue, Project
from projects.permissions import IsAuthorOrReadOnly, IsContributor
from projects.serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gère le CRUD des Projets.
    Seuls les contributeurs peuvent lire, seul l'auteur peut modifier/supprimer.
    """
    serializer_class = ProjectSerializer
    # Utilisation d'un tuple () au lieu d'une liste [] pour éviter l'avertissement Ruff (RUF012)
    permission_classes = (IsAuthenticated, IsContributor, IsAuthorOrReadOnly)

    def get_queryset(self):
        # Filtre : un utilisateur ne voit que les projets dont il est contributeur
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        # À la création, l'utilisateur connecté est défini comme auteur
        project = serializer.save(author=self.request.user)
        # L'auteur est automatiquement ajouté comme premier contributeur du projet
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Gère les contributeurs d'un projet spécifique.
    """
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, IsContributor, IsAuthorOrReadOnly)

    def get_queryset(self):
        # Récupère uniquement les contributeurs rattachés au projet dans l'URL
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        # Associe automatiquement le nouveau membre au projet spécifié dans l'URL
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    """
    Gère les tickets (Issues) d'un projet.
    """
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IsContributor, IsAuthorOrReadOnly)

    def get_queryset(self):
        # Récupère les tickets du projet spécifié dans l'URL
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        # Définit l'auteur sur l'utilisateur connecté et lie la demande au projet
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Gère les commentaires rattachés à un ticket (Issue).
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsContributor, IsAuthorOrReadOnly)

    def get_queryset(self):
        # Récupère uniquement les commentaires du ticket spécifié dans l'URL
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        # Définit l'auteur et associe le commentaire au ticket courant
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(author=self.request.user, issue=issue)