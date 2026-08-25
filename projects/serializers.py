from rest_framework import serializers

from authentication.serializers import UserSerializer
from projects.models import Comment, Contributor, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création et la consultation des projets.

    L'auteur est renseigné automatiquement à partir de l'utilisateur connecté.
    """

    # Représentation imbriquée et en lecture seule de l'auteur du projet
    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        # Champs bloqués en écriture pour garantir la traçabilité et la sécurité
        read_only_fields = ("id", "author", "created_time")


class ContributorSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des membres rattachés à un projet."""

    # Champ personnalisé pour afficher les détails complets de l'utilisateur contributeur
    user_detail = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Contributor
        fields = "__all__"
        # Le projet parent et l'horodatage sont automatiques et non modifiables
        read_only_fields = ("id", "project", "created_time")


class IssueSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des tickets (Issues).

    L'auteur et le projet référencé sont gérés automatiquement en lecture seule.
    """

    # Auteur affiché sous forme d'objet utilisateur détaillé
    author = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"
        # Empêche la modification de l'ID, du projet d'attachement, de l'auteur et de la date
        read_only_fields = ("id", "project", "author", "created_time")


class CommentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les commentaires de tickets."""

    # Auteur affiché sous forme d'objet utilisateur détaillé
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        # Sécurise l'UUID, l'issue liée, l'auteur et l'horodatage en lecture seule
        read_only_fields = ("id", "uuid", "issue", "author", "created_time")