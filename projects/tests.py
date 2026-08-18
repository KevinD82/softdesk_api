from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from projects.models import Contributor, Issue, Project


class ProjectAndPermissionsAPITests(APITestCase):
    """
    Tests unitaires pour l'application projects.
    Vérifie les permissions d'accès (contributeurs vs non-contributeurs)
    et les droits d'édition/suppression réservés à l'auteur (règles OWASP).
    """

    def setUp(self):
        """Préparation du jeu de données en mémoire pour chaque test."""
        # 1. Création de trois utilisateurs distincts
        self.user_author = User.objects.create_user(
            username="author_user",
            password="Password123!",
            birth_date="1995-01-01"
        )
        self.user_contrib = User.objects.create_user(
            username="contrib_user",
            password="Password123!",
            birth_date="1995-01-01"
        )
        self.user_stranger = User.objects.create_user(
            username="stranger_user",
            password="Password123!",
            birth_date="1995-01-01"
        )

        # 2. Création d'un projet appartenant à user_author
        self.project = Project.objects.create(
            name="Projet Alpha",
            description="Projet de test",
            type="BACKEND",
            author=self.user_author
        )
        
        # 3. Association des contributeurs au projet
        Contributor.objects.create(user=self.user_author, project=self.project)
        Contributor.objects.create(user=self.user_contrib, project=self.project)

        # 4. Création d'une issue par l'auteur du projet
        self.issue = Issue.objects.create(
            title="Issue initiale",
            description="Description issue",
            priority="HIGH",
            tag="BUG",
            status="TO_DO",
            project=self.project,
            author=self.user_author
        )

    def test_stranger_cannot_access_project(self):
        """Vérifie qu'un utilisateur non-contributeur ne peut pas voir le projet (HTTP 404)."""
        # Authentification en tant qu'utilisateur externe
        self.client.force_authenticate(user=self.user_stranger)
        url = reverse("projects-detail", kwargs={"pk": self.project.pk})
        
        response = self.client.get(url)
        # Pour des raisons de sécurité, le projet renvoie 404 au lieu de 403 pour masquer son existence
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contributor_can_read_project_issues(self):
        """Vérifie qu'un membre/contributeur accède à la liste des tickets du projet (HTTP 200)."""
        # Authentification du membre
        self.client.force_authenticate(user=self.user_contrib)
        url = reverse("project-issues-list", kwargs={"project_pk": self.project.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contributor_cannot_update_author_issue(self):
        """Vérifie qu'un contributeur ne peut pas modifier un ticket créé par l'auteur (HTTP 403)."""
        # Authentification du membre non-auteur du ticket
        self.client.force_authenticate(user=self.user_contrib)
        url = reverse(
            "project-issues-detail",
            kwargs={"project_pk": self.project.pk, "pk": self.issue.pk}
        )
        data = {"title": "Titre modifié sans permission"}
        
        response = self.client.patch(url, data)
        # L'accès est refusé car seul l'auteur possède les droits d'écriture
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_and_delete_comment_by_author(self):
        """Vérifie le cycle de vie d'un commentaire : création puis suppression par son auteur."""
        self.client.force_authenticate(user=self.user_contrib)
        
        # 1. Création du commentaire
        create_url = reverse(
            "issue-comments-list",
            kwargs={"project_pk": self.project.pk, "issue_pk": self.issue.pk}
        )
        create_response = self.client.post(create_url, {"description": "Mon avis"})
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Récupération de la clé primaire renvoyée par le sérialiseur
        # On vérifie d'abord 'uuid', puis 'id'
        comment_id = create_response.data.get("uuid") or create_response.data.get("id")
        self.assertIsNotNone(comment_id, "L'identifiant du commentaire ne doit pas être None")

        # 2. Suppression du commentaire par son auteur
        delete_url = reverse(
            "issue-comments-detail",
            kwargs={
                "project_pk": self.project.pk,
                "issue_pk": self.issue.pk,
                "pk": comment_id
            }
        )
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)