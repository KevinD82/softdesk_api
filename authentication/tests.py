from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User


class AuthenticationAPITests(APITestCase):
    """
    Tests unitaires pour l'application authentication.
    Vérifie l'inscription, la conformité RGPD (âge minimum) et la connexion JWT.
    """

    def setUp(self):
        """Configuration initiale exécutée avant chaque méthode de test."""
        # Résolution des URLs des points de terminaison via leur nom
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        
        # Données de référence pour la création d'un utilisateur valide
        self.valid_payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "Password123!",
            "birth_date": "2000-01-01",
            "can_be_contacted": True,
            "can_data_be_shared": False,
        }

    def test_signup_success(self):
        """Vérifie qu'un utilisateur valide peut créer un compte (HTTP 201)."""
        response = self.client.post(self.signup_url, self.valid_payload)
        
        # Le serveur doit répondre avec un statut HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # L'utilisateur doit être effectivement créé en base de données
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_signup_underage_fails(self):
        """Vérifie la restriction RGPD : rejet des utilisateurs de moins de 15 ans (HTTP 400)."""
        payload = self.valid_payload.copy()
        payload["username"] = "youngster"
        # Date de naissance configurée pour avoir moins de 15 ans
        payload["birth_date"] = "2020-01-01"

        response = self.client.post(self.signup_url, payload)
        
        # La requête doit être rejetée avec une erreur Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # La réponse doit spécifier que l'erreur provient du champ birth_date
        self.assertIn("birth_date", response.data)

    def test_login_jwt(self):
        """Vérifie que la connexion renvoie un couple de tokens JWT (access et refresh)."""
        # Création préalable de l'utilisateur
        User.objects.create_user(**self.valid_payload)
        login_data = {"username": "alice", "password": "Password123!"}
        
        response = self.client.post(self.login_url, login_data)
        
        # Connexion réussie HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Présence des deux clés de jetons dans la réponse JSON
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)