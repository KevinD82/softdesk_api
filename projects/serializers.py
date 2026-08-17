from rest_framework import serializers

from authentication.serializers import UserSerializer
from projects.models import Comment, Contributor, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création et la consultation des projets.
    L'auteur est renseigné automatiquement à partir de l'utilisateur connecté.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("id", "author", "created_time")


class ContributorSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la gestion des membres rattachés à un projet.
    """

    user_detail = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Contributor
        fields = "__all__"
        read_only_fields = ("id", "project", "created_time")


class IssueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la gestion des tickets (Issues).
    L'auteur et le projet référencé sont gérés automatiquement en lecture seule.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ("id", "project", "author", "created_time")


class CommentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les commentaires de tickets.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "uuid", "issue", "author", "created_time")
