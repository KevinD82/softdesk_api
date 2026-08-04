# SoftDesk API

SoftDesk est une API REST sécurisée développée avec **Django REST Framework (DRF)** permettant de gérer des projets informatiques, leurs contributeurs, des tickets d'incidents (issues) et des commentaires.

Le projet respecte les normes du **RGPD** pour l'inscription des utilisateurs (âge minimal de 15 ans et recueil des consentements) et s'appuie sur une authentification par jeton **JWT**.

---

##  Stack Technique

* **Langage :** Python 3.12+
* **Framework :** Django 5.x & Django REST Framework (DRF)
* **Gestionnaire de dépendances :** Poetry
* **Base de données :** SQLite (développement)
* **Authentification :** JWT (`django-rest-framework-simplejwt`)

---

##  Installation et Configuration

### 1. Prérequis
Assure-toi d'avoir **Python 3.12+** et **Poetry** installés sur ta machine.

### 2. Cloner le projet et installer les dépendances
```powershell
# Déplacements dans le répertoire du projet
cd softdesk_api

# Installation les dépendances
```powershell
pip install poetry

poetry install
```
# Gestion de la Base de Données & Migrations

Toutes les commandes doivent être exécutées via l'environnement virtuel géré par Poetry.
1. Générer les fichiers de migration
```PowerShell
# Migration globale
poetry run python manage.py makemigrations

```
2. Appliquer les migrations sur la base SQLite
```PowerShell
poetry run python manage.py migrate
```

3. Réinitialiser la base de données (si nécessaire en dev)
```PowerShell
# Supprimer la base SQLite et régénérer
Remove-Item db.sqlite3 -ErrorAction Ignore

poetry run python manage.py migrate
```

4. Lancement de l'Application
# Pour démarrer le serveur de développement Django :
```PowerShell
Poetry run python manage.py runserver
```
L'API sera accessible sur : http://127.0.0.1:8000/

 Endpoints d'Authentification (Fonctionnels)
1. Inscription d'un utilisateur (POST /api/signup/)
Body (JSON) :
```JSON{
    "username": "kev_dev",
    "email": "kev@softdesk.com",
    "password": "Password123!",
    "birth_date": "1998-05-12",
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```
Contrainte RGPD : L'utilisateur doit être âgé d'au moins 15 ans.

2. Connexion / Obtention du Token JWT (POST /api/login/)
Body (JSON) :
```JSON{
    "username": "kev_dev",
    "password": "Password123!"
}
```
Réponse : Retourne un jeton access et un jeton refresh.3. Rafraîchissement du Token (POST /api/token/refresh/)Body (JSON) :JSON{
    "refresh": "<VOTRE_REFRESH_TOKEN>"
}
```

 Structure Actuelle des Modèles (projects/models.py)
- User (Custom) : username, email, birth_date, can_be_contacted, can_data_be_shared
- Project : name, description, type (Backend, Frontend, iOS, Android), author
- Contributor : Relation unique user $\leftrightarrow$ project
- Issue : title, description, priority, tag, status, project, author, assigned_to
- Comment : description, issue, author
```

---

### Endpoints Ressources (CRUD)

## Projets (/api/projects/)
GET /api/projects/ : Lister les projets dont l'utilisateur est auteur ou contributeur.

POST /api/projects/ : Créer un nouveau projet (l'utilisateur connecté est automatiquement défini comme auteur).

GET /api/projects/{project_id}/ : Obtenir les détails d'un projet.

PUT /api/projects/{project_id}/ / PATCH : Mettre à jour un projet (Auteur uniquement).

DELETE /api/projects/{project_id}/ : Supprimer un projet (Auteur uniquement).

## Contributeurs (/api/projects/{project_id}/users/)
GET /api/projects/{project_id}/users/ : Lister les contributeurs d'un projet.

POST /api/projects/{project_id}/users/ : Ajouter un utilisateur comme contributeur au projet.

DELETE /api/projects/{project_id}/users/{user_id}/ : Retirer un contributeur du projet.

## Tickets / Issues (/api/projects/{project_id}/issues/)
GET /api/projects/{project_id}/issues/ : Lister les tickets associés à un projet.

POST /api/projects/{project_id}/issues/ : Créer un ticket lié à un projet.

GET /api/projects/{project_id}/issues/{issue_id}/ : Obtenir les détails d'un ticket.

PUT /api/projects/{project_id}/issues/{issue_id}/ / PATCH : Mettre à jour un ticket (Auteur uniquement).

DELETE /api/projects/{project_id}/issues/{issue_id}/ : Supprimer un ticket (Auteur uniquement).

## Commentaires (/api/projects/{project_id}/issues/{issue_id}/comments/)
GET /api/projects/{project_id}/issues/{issue_id}/comments/ : Lister les commentaires d'un ticket.

POST /api/projects/{project_id}/issues/{issue_id}/comments/ : Ajouter un commentaire sur un ticket.

GET /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/ : Obtenir les détails d'un commentaire.

PUT /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/ / PATCH : Modifier un commentaire (Auteur uniquement).

DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/ : Supprimer un commentaire (Auteur uniquement).

## Architecture des Modèles
User (Custom) : username, email, birth_date, can_be_contacted, can_data_be_shared

Project : name, description, type (Backend, Frontend, iOS, Android), author

Contributor : Relation unique user ↔ project

Issue : title, description, priority (LOW, MEDIUM, HIGH), tag (BUG, FEATURE, TASK), status (To Do, In Progress, Finished), project, author, assigned_to

Comment : description, issue, author, created_time