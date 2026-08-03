# SoftDesk API

SoftDesk est une API REST sécurisée développée avec **Django REST Framework (DRF)** permettant de gérer des projets informatiques, leurs contributeurs, des tickets d'incidents (issues) et des commentaires.

Le projet respecte les normes du **RGPD** pour l'inscription des utilisateurs (âge minimal de 15 ans et recueil des consentements) et s'appuie sur une authentification par jeton **JWT**.

---

## 🛠️ Stack Technique

* **Langage :** Python 3.12+
* **Framework :** Django 5.x & Django REST Framework (DRF)
* **Gestionnaire de dépendances :** Poetry
* **Base de données :** SQLite (développement)
* **Authentification :** JWT (`django-rest-framework-simplejwt`)

---

## 🚀 Installation et Configuration

### 1. Prérequis
Assure-toi d'avoir **Python 3.12+** et **Poetry** installés sur ta machine.

### 2. Cloner le projet et installer les dépendances
```powershell
# Déplacements dans le répertoire du projet
cd softdesk_api

# Installation des dépendances via Poetry
poetry install
```
# Gestion de la Base de Données & Migrations

Toutes les commandes doivent être exécutées via l'environnement virtuel géré par Poetry.
1. Générer les fichiers de migration
```PowerShell
# Migration globale
poetry run python manage.py makemigrations

# Ou spécifiquement par application
poetry run python manage.py makemigrations authentication

poetry run python manage.py makemigrations projects
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

💻 Lancement de l'Application
Pour démarrer le serveur de développement Django :
```PowerShell
Poetry run python manage.py runserver
```
L'API sera accessible sur : http://127.0.0.1:8000/

📌 Endpoints d'Authentification (Fonctionnels)
1. Inscription d'un utilisateur (POST /api/signup/)
Body (JSON) :
```JSON{
    "username": "alex_dev",
    "email": "alex@softdesk.com",
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
    "username": "alex_dev",
    "password": "Password123!"
}
```
Réponse : Retourne un jeton access et un jeton refresh.3. Rafraîchissement du Token (POST /api/token/refresh/)Body (JSON) :JSON{
    "refresh": "<VOTRE_REFRESH_TOKEN>"
}
📐 Structure Actuelle des Modèles (projects/models.py)
- User (Custom) : username, email, birth_date, can_be_contacted, can_data_be_shared
- Project : name, description, type (Backend, Frontend, iOS, Android), author
- Contributor : Relation unique user $\leftrightarrow$ project
- Issue : title, description, priority, tag, status, project, author, assigned_to
- Comment : description, issue, author
---

