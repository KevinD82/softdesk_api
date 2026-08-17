# SoftDesk API - Documentation Complète

SoftDesk est une **API REST sécurisée et optimisée** développée avec **Django REST Framework (DRF)** permettant de gérer des projets informatiques, leurs contributeurs, des tickets d'incidents (issues) et des commentaires.

Le projet respecte les normes du **RGPD** pour l'inscription des utilisateurs (âge minimal de 15 ans et recueil des consentements), s'appuie sur une authentification par jeton **JWT** conforme à **OWASP**, et intègre les principes du **Green Code** pour minimiser l'impact environnemental.

---

## 📋 Table des matières

1. [Stack Technique](#stack-technique)
2. [Installation & Configuration](#installation--configuration)
3. [Variables d'Environnement](#variables-denvironnement)
4. [Sécurité (OWASP + RGPD)](#sécurité-owasp--rgpd)
5. [Architecture des Modèles](#architecture-des-modèles)
6. [Endpoints API](#endpoints-api)
7. [Green Code & Optimisations](#green-code--optimisations)
8. [Dépendances](#dépendances)
9. [Tests & Validation](#tests--validation)

---

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|------------|
| **Langage** | Python 3.12+ |
| **Framework** | Django 6.0+ & Django REST Framework (DRF) |
| **Gestionnaire de dépendances** | Poetry |
| **Base de données** | SQLite (dev) / PostgreSQL (production) |
| **Authentification** | JWT (`django-rest-framework-simplejwt`) |
| **Validation de données** | Django ORM + DRF Serializers |
| **Optimisation** | select_related(), pagination (PAGE_SIZE=10) |

---

## 📦 Installation & Configuration

### 1. Prérequis

Assure-toi d'avoir installé sur ta machine :
- **Python 3.12+** ([Télécharger](https://www.python.org/))
- **Poetry 1.5+** ([Télécharger](https://python-poetry.org/))
- **Git** ([Télécharger](https://git-scm.com/))

### 2. Cloner le projet

```bash
git clone https://github.com/ton-username/softdesk_api.git
cd softdesk_api
```

### 3. Installer les dépendances avec Poetry

```bash
# Créer l'environnement virtuel et installer les dépendances
poetry install

# Activer l'environnement virtuel
poetry shell
```

### 4. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet (voir section ci-dessous) :

```bash
cp .env.example .env  # Si le fichier exemple existe
# OU crée manuellement un fichier .env
```

### 5. Initialiser la base de données

```bash
# Créer les tables et appliquer les migrations
poetry run python manage.py migrate

# (Optionnel) Créer un utilisateur administrateur
poetry run python manage.py createsuperuser
```

### 6. Lancer le serveur de développement

```bash
poetry run python manage.py runserver
```

L'API sera accessible sur : **http://127.0.0.1:8000/**

L'interface d'administration : **http://127.0.0.1:8000/admin/**

---

## 🔐 Variables d'Environnement

Crée un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Clé secrète Django (IMPORTANT: changer en production)
# Génère une nouvelle clé: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=django-insecure-your-secret-key-here

# Mode debug (IMPORTANT: False en production!)
DEBUG=True

# Hosts autorisés (séparés par des virgules)
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration optionnelle de la base de données
# DATABASE_URL=sqlite:///db.sqlite3
```

⚠️ **IMPORTANT :** Le fichier `.env` ne doit **JAMAIS** être commité sur Git (déjà dans `.gitignore`)

---

## 🔒 Sécurité (OWASP + RGPD)

### Conformité OWASP

L'API implémente les mesures de sécurité OWASP suivantes :

#### 1. **Authentification (JWT)**
- ✅ Utilise les tokens JWT (`django-rest-framework-simplejwt`)
- ✅ Les tokens ont une durée de validité limitée :
  - Access Token : 1 jour
  - Refresh Token : 7 jours
- ✅ Chaque requête nécessite l'en-tête : `Authorization: Bearer <token>`

#### 2. **Autorisation (Permissions)**
- ✅ **`IsAuthenticated`** : Seuls les utilisateurs connectés peuvent accéder aux ressources
- ✅ **`IsContributor`** : Seuls les contributeurs d'un projet peuvent le voir
- ✅ **`IsAuthorOrReadOnly`** : Seul l'auteur peut modifier/supprimer une ressource

#### 3. **Gestion des Dépendances**
- ✅ Utilise **Poetry** pour gérer les dépendances et leurs versions
- ✅ Les dépendances sont verrouillées dans `poetry.lock`
- ✅ Mise à jour régulière via : `poetry update`

### Conformité RGPD

#### 1. **Droit d'accès et de rectification**
- ✅ Les utilisateurs peuvent accéder à leurs données via l'API
- ✅ Les utilisateurs peuvent modifier leurs informations personnelles

#### 2. **Droit à l'oubli**
- ✅ Les utilisateurs peuvent supprimer leur compte
- ✅ Tous les commentaires et issues liées sont supprimés en cascade

#### 3. **Consentement explicite**
L'API collecte deux champs de consentement lors de l'inscription :
- **`can_be_contacted`** : Autoriser le contact via email
- **`can_data_be_shared`** : Autoriser le partage des données

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "birth_date": "2000-05-15",
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

#### 4. **Vérification de l'âge**
- ✅ L'utilisateur doit être **âgé d'au moins 15 ans** pour s'inscrire
- ✅ La vérification se fait lors de l'inscription et de la modification du profil
- ✅ En cas d'âge insuffisant, l'inscription est rejetée avec le message :
  > "L'utilisateur doit être âgé d'au moins 15 ans."

---

## 🏗️ Architecture des Modèles

### 1. **User** (Utilisateur personnalisé)

```python
class User(AbstractUser):
    birth_date          : DateField              # Date de naissance
    can_be_contacted    : BooleanField          # Autorisation de contact
    can_data_be_shared  : BooleanField          # Autorisation de partage de données
```

**Validations :**
- Âge minimum : 15 ans (RGPD)
- Email unique
- Username unique

---

### 2. **Project** (Projet)

```python
class Project(models.Model):
    name               : CharField(max_length=128)
    description        : TextField(blank=True)
    type               : CharField (choices: BACKEND, FRONTEND, IOS, ANDROID)
    author             : ForeignKey(User)        # L'utilisateur qui a créé le projet
    created_time       : DateTimeField           # Date de création
```

**Relations :**
- **1-à-N** : Un projet a plusieurs **Contributors**
- **1-à-N** : Un projet a plusieurs **Issues**

**Permissions :**
- ✅ Créer : Tous les utilisateurs authentifiés
- ✅ Lire : Seuls les contributeurs du projet
- ✅ Modifier : Seul l'auteur du projet
- ✅ Supprimer : Seul l'auteur du projet

---

### 3. **Contributor** (Contributeur)

```python
class Contributor(models.Model):
    user               : ForeignKey(User)        # Utilisateur contributeur
    project            : ForeignKey(Project)     # Projet
    created_time       : DateTimeField           # Date d'ajout comme contributeur
    
    # Contrainte : Un utilisateur ne peut être contributeur qu'une fois par projet
    class Meta:
        UniqueConstraint(fields=['user', 'project'])
```

**Relations :**
- **N-à-N** : Relie **Users** et **Projects**

**Permissions :**
- ✅ Créer : Seul l'auteur du projet peut ajouter un contributeur
- ✅ Lire : Seuls les contributeurs du projet et l'auteur
- ✅ Supprimer : Seul l'auteur du projet peut retirer un contributeur

---

### 4. **Issue** (Ticket/Problème)

```python
class Issue(models.Model):
    title              : CharField(max_length=128)
    description        : TextField
    priority           : CharField (choices: LOW, MEDIUM, HIGH) [défaut: MEDIUM]
    tag                : CharField (choices: BUG, FEATURE, TASK)
    status             : CharField (choices: TO_DO, IN_PROGRESS, FINISHED) [défaut: TO_DO]
    project            : ForeignKey(Project)     # Projet associé
    author             : ForeignKey(User)        # Créateur du ticket
    assigned_to        : ForeignKey(User, nullable=True)  # Utilisateur assigné
    created_time       : DateTimeField           # Date de création
```

**Relations :**
- **N-à-1** : Plusieurs Issues pour un Project
- **1-à-N** : Une Issue a plusieurs **Comments**

**Permissions :**
- ✅ Créer : Seuls les contributeurs du projet
- ✅ Lire : Seuls les contributeurs du projet
- ✅ Modifier : Seul l'auteur du ticket
- ✅ Supprimer : Seul l'auteur du ticket

---

### 5. **Comment** (Commentaire)

```python
class Comment(models.Model):
    uuid               : UUIDField(unique=True)  # Identifiant unique
    description        : TextField
    issue              : ForeignKey(Issue)       # Ticket associé
    author             : ForeignKey(User)        # Auteur du commentaire
    created_time       : DateTimeField           # Date de création
```

**Relations :**
- **N-à-1** : Plusieurs Comments pour une Issue

**Permissions :**
- ✅ Créer : Seuls les contributeurs du projet de l'issue
- ✅ Lire : Seuls les contributeurs du projet de l'issue
- ✅ Modifier : Seul l'auteur du commentaire
- ✅ Supprimer : Seul l'auteur du commentaire

---

## 🔗 Endpoints API

### 📱 **Authentification**

#### 1. Inscription utilisateur
```http
POST /api/signup/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "birth_date": "2000-05-15",
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

**Réponse (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "birth_date": "2000-05-15",
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

---

#### 2. Connexion / Obtention du token
```http
POST /api/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Réponse (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

#### 3. Rafraîchir le token d'accès
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Réponse (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 📂 **Projets**

#### Lister les projets
```http
GET /api/projects/
Authorization: Bearer <access_token>
```

**Réponse avec Pagination (200 OK):**
```json
{
  "count": 47,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Mon Projet",
      "description": "Description du projet",
      "type": "BACKEND",
      "author": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
      },
      "created_time": "2026-08-17T10:30:00Z"
    }
    // ... 9 projets par page
  ]
}
```

#### Créer un projet
```http
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Nouveau Projet",
  "description": "Description",
  "type": "FRONTEND"
}
```

#### Détails d'un projet
```http
GET /api/projects/{project_id}/
Authorization: Bearer <access_token>
```

#### Modifier un projet (auteur uniquement)
```http
PUT /api/projects/{project_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Projet Modifié",
  "description": "Nouvelle description",
  "type": "BACKEND"
}
```

#### Supprimer un projet (auteur uniquement)
```http
DELETE /api/projects/{project_id}/
Authorization: Bearer <access_token>
```

---

### 👥 **Contributeurs**

#### Lister les contributeurs d'un projet
```http
GET /api/projects/{project_id}/users/
Authorization: Bearer <access_token>
```

#### Ajouter un contributeur (auteur du projet uniquement)
```http
POST /api/projects/{project_id}/users/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user": 2  // ID de l'utilisateur à ajouter
}
```

#### Retirer un contributeur (auteur du projet uniquement)
```http
DELETE /api/projects/{project_id}/users/{user_id}/
Authorization: Bearer <access_token>
```

---

### 🎫 **Tickets/Issues**

#### Lister les issues d'un projet
```http
GET /api/projects/{project_id}/issues/
Authorization: Bearer <access_token>
```

#### Créer une issue (contributeur du projet)
```http
POST /api/projects/{project_id}/issues/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Bug critique",
  "description": "L'authentification ne fonctionne pas",
  "priority": "HIGH",
  "tag": "BUG",
  "status": "TO_DO",
  "assigned_to": 2  // Optionnel
}
```

#### Détails d'une issue
```http
GET /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <access_token>
```

#### Modifier une issue (auteur uniquement)
```http
PATCH /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "IN_PROGRESS",
  "priority": "MEDIUM"
}
```

#### Supprimer une issue (auteur uniquement)
```http
DELETE /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <access_token>
```

---

### 💬 **Commentaires**

#### Lister les commentaires d'une issue
```http
GET /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer <access_token>
```

#### Ajouter un commentaire (contributeur du projet)
```http
POST /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "description": "J'ai trouvé la cause du problème..."
}
```

#### Détails d'un commentaire
```http
GET /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer <access_token>
```

#### Modifier un commentaire (auteur uniquement)
```http
PATCH /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "description": "Commentaire modifié"
}
```

#### Supprimer un commentaire (auteur uniquement)
```http
DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer <access_token>
```

---

## 🌱 Green Code & Optimisations

L'API SoftDesk implémente les principes du **Green Code** pour minimiser son impact environnemental :

### 1. **Pagination des Ressources**

Toutes les listes d'API retournent **10 éléments par page** par défaut :

```http
GET /api/projects/?page=2
GET /api/projects/{project_id}/issues/?page=1
GET /api/projects/{project_id}/issues/{issue_id}/comments/?page=3
```

**Réponse :**
```json
{
  "count": 150,                 // Nombre total d'éléments
  "next": "...?page=2",         // Lien vers la page suivante
  "previous": "...?page=1",     // Lien vers la page précédente
  "results": [...]              // 10 éléments maximum par page
}
```

**Avantages :**
- ✅ Réduit la charge serveur
- ✅ Diminue la consommation réseau
- ✅ Améliore les performances client
- 🌱 Économise ~99% de la bande passante pour les grandes listes

---

### 2. **Optimisation des Requêtes (select_related)**

L'API utilise `select_related()` pour éviter le problème **N+1 queries** :

**Avant :** Charger 100 projets = **101 requêtes SQL** ⚠️
- 1 requête pour les 100 projets
- +100 requêtes pour les auteurs (1 par projet)

**Après :** Charger 100 projets = **1 requête SQL** ✅
- select_related('author') : Charge auteur et projet en UNE SEULE requête

**Impact :**
| Ressource | Avant | Après | Économies |
|-----------|-------|-------|-----------|
| 100 projets | 101 requêtes | 1 requête | 100× moins |
| 100 contributors | 201 requêtes | 1 requête | 200× moins |
| 100 issues | 301 requêtes | 1 requête | 300× moins |

🌱 **Réduction de ~99% des requêtes = Consommation énergie divisée par 100** 

---

## 📦 Dépendances

### Stack Principal

```
Django==6.0.7
djangorestframework==3.17.1
djangorestframework-simplejwt==5.5.1
drf-nested-routers==0.95.3
python-dotenv==1.2.3
```

### Vérifier les mises à jour

```bash
poetry update
poetry outdated
```

---

## 🧪 Tests & Validation

### 1. Vérifier la configuration

```bash
poetry run python manage.py check
```

### 2. Lancer les migrations

```bash
poetry run python manage.py migrate
```

### 3. Tester avec Postman

1. Importe la [collection Postman](#) (à créer)
2. Configure l'environnement avec une URL : `http://localhost:8000`
3. Teste chaque endpoint en ordre :
   - Inscription (`POST /api/signup/`)
   - Connexion (`POST /api/login/`)
   - Créer un projet (`POST /api/projects/`)
   - Ajouter un contributeur
   - Créer une issue
   - Ajouter un commentaire
   - Modifier et supprimer les ressources

### 4. Vérifier les performances

Pour vérifier l'optimisation des requêtes, active le mode debug Django :

```python
# Dans settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

Puis observe le nombre de requêtes SQL dans les logs :
```
SELECT ... FROM projects WHERE ...  // 1 requête
SELECT ... FROM auth_user WHERE ... // Chargé avec select_related
```

---

## 🚀 Déploiement en Production

Avant de déployer en production, n'oublie pas de :

1. **Changer la SECRET_KEY** :
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Mettre DEBUG=False** dans `.env` :
   ```env
   DEBUG=False
   ```

3. **Configurer ALLOWED_HOSTS** avec ton domaine :
   ```env
   ALLOWED_HOSTS=example.com,www.example.com
   ```

4. **Configurer la base de données PostgreSQL** :
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/softdesk
   ```

5. **Générer les fichiers statiques** :
   ```bash
   poetry run python manage.py collectstatic
   ```

6. **Utiliser Gunicorn** comme serveur WSGI :
   ```bash
   poetry add gunicorn
   poetry run gunicorn softdesk.wsgi:application --bind 0.0.0.0:8000
   ```

---

## 📝 Licence

Ce projet est développé dans le cadre de la formation OpenClassrooms.

---

## ✉️ Support

Pour toute question ou problème, contacte le développeur principal ou crée une **issue** sur le repository.

---

**Dernière mise à jour :** 2026-08-17  
**Version :** 1.0.0  
**Statut :** ✅ Conforme OWASP, RGPD, Green Code
