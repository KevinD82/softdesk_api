# SoftDesk API

SoftDesk est une API REST sécurisée et optimisée développée avec Django REST Framework (DRF) pour la gestion de projets informatiques, de contributeurs, de tickets d'incidents (issues) et de commentaires.

Le projet intègre une authentification JWT conforme aux recommandations OWASP, respecte les exigences du RGPD (âge minimum de 15 ans et consentement explicite), et applique les principes du Green Code (pagination et optimisation des requêtes SQL).

---

## 📋 Table des matières

1. [Stack Technique](#️-stack-technique)
2. [Installation & Configuration](#-installation--configuration)
3. [Variables d'Environnement](#-variables-denvironnement)
4. [Sécurité & Conformité](#️-sécurité--conformité)
5. [Endpoints API](#-endpoints-api-principaux)
6. [Guide de Test Postman](#-guide-de-test-postman)
7. [Green Code & Optimisations](#-green-code--optimisations)
8. [Qualité & Tests](#-qualité--tests)

---

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|------------|
| **Langage** | Python 3.12+ |
| **Framework** | Django 5.x & Django REST Framework (DRF) |
| **Gestionnaire de dépendances** | Poetry 1.8+ |
| **Base de données** | SQLite (développement) / PostgreSQL (production) |
| **Authentification** | JWT (djangorestframework-simplejwt) |
| **Routage imbriqué** | drf-nested-routers |

---

## 📦 Installation & Configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-username/softdesk_api.git
cd softdesk_api
```

### 2. Installer les dépendances avec Poetry

```bash
poetry install
```

### 3. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet en t'inspirant de la section suivante.

### 4. Appliquer les migrations & lancer le serveur

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

L'API est accessible sur : `http://127.0.0.1:8000/`

---

## 🔐 Variables d'Environnement

Crée un fichier `.env` à la racine :

```env
SECRET_KEY=ta-cle-secrete-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🛡️ Sécurité & Conformité

- **Authentification JWT** : Jetons d'accès (1 jour) et de rafraîchissement (7 jours).
- **Permissions granulaires** : Accès restreint par rôles.

| Permission | Accès autorisé |
|---|---|
| `IsAuthenticated` | Requiert un utilisateur connecté pour toute action |
| `IsContributor` | Lecture/écriture réservée aux contributeurs du projet concerné |
| `IsAuthorOrReadOnly` | Modification/suppression réservées à l'auteur de la ressource ; lecture seule pour les autres |

- **Conformité RGPD** :
  - Vérification de l'âge minimum de 15 ans à l'inscription.
  - Recueil des consentements explicites (`can_be_contacted`, `can_data_be_shared`).
  - Suppression en cascade des données personnelles en cas de suppression de compte.

---

## 🔗 Endpoints API principaux

- **Authentification & Utilisateurs** :
  - `POST /api/signup/` : Inscription d'un utilisateur
  - `POST /api/login/` : Connexion (obtention des tokens JWT)
  - `POST /api/token/refresh/` : Rafraîchissement du token d'accès
- **Projets** (`/api/projects/`) : CRUD complet des projets.
- **Contributeurs** (`/api/projects/{project_id}/users/`) : Gestion des contributeurs d'un projet.
- **Tickets / Issues** (`/api/projects/{project_id}/issues/`) : Gestion des tickets d'incidents.
- **Commentaires** (`/api/projects/{project_id}/issues/{issue_id}/comments/`) : Gestion des commentaires associés aux tickets.

### Gestion des erreurs

L'API retourne des codes HTTP standards accompagnés d'un corps JSON explicite :

| Code | Signification |
|---|---|
| `400` | Requête invalide (champ manquant, format incorrect) |
| `401` | Authentification requise ou token invalide/expiré |
| `403` | Action non autorisée pour l'utilisateur courant |
| `404` | Ressource introuvable |

---

## 📮 Guide de Test Postman

Pour tester facilement l'API avec Postman, procédez dans cet ordre :

### 1. Variables d'environnement Postman recommandées

Créez un environnement dans Postman avec les variables suivantes :
- `url` : `http://127.0.0.1:8000`
- `access_token` : (laisser vide, sera rempli automatiquement ou manuellement)

### 2. Séquence de test pas à pas

1. **Inscription d'un utilisateur** (`POST {{url}}/api/signup/`)

   **Body (JSON)** :
   ```json
   {
       "username": "johndoe",
       "password": "SecurePassword123!",
       "first_name": "John",
       "last_name": "Doe",
       "birth_date": "1995-06-15",
       "can_be_contacted": true,
       "can_data_be_shared": true
   }
   ```

2. **Connexion / Obtention du Token** (`POST {{url}}/api/login/`)

   **Body (JSON)** :
   ```json
   {
       "username": "johndoe",
       "password": "SecurePassword123!"
   }
   ```

   **Réponse attendue** :
   ```json
   {
       "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
       "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }
   ```

   *Astuce* : Copiez la valeur du champ `access` retourné par l'API.

3. **Authentification des requêtes suivantes**

   Pour toutes les routes protégées, allez dans l'onglet **Authorization** de Postman, sélectionnez **Bearer Token** et collez votre `access_token`.

4. **Création d'un projet** (`POST {{url}}/api/projects/`)

   **Body (JSON)** :
   ```json
   {
       "title": "Mon Premier Projet",
       "description": "Description du projet SoftDesk",
       "type": "BACK-END"
   }
   ```

---

## 🌱 Green Code & Optimisations

- **Pagination centralisée** : Fixée à 10 éléments par page pour limiter la consommation de bande passante et la charge serveur.
- **Optimisation des requêtes SQL** : Utilisation systématique de `select_related()` pour éliminer le problème des requêtes N+1.

---

## 🧪 Tests & Validation

### Contrôle qualité (Ruff)


# Vérifier la qualité du code
```bash
poetry run ruff check .
```
# Formater le code
```bash
poetry run ruff format .
```

Pour exécuter la suite de tests unitaires :

```bash
poetry run python manage.py test
```
