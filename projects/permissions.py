from rest_framework import permissions

from projects.models import Contributor, Project


class IsContributor(permissions.BasePermission):
    """
    Permission personnalisée : vérifie si l'utilisateur est un contributeur du projet.
    """

    def has_permission(self, request, view):
        # 1. L'utilisateur doit obligatoirement être connecté
        if not (request.user and request.user.is_authenticated):
            return False

        # 2. Si l'action concerne la création d'un projet (POST sur ProjectViewSet),
        # tout utilisateur connecté est autorisé
        if view.basename == 'projects' and request.method == 'POST':
            return True

        return True

    def has_object_permission(self, request, view, obj):
        # Récupération du projet selon le type d'objet (Project, Issue, Comment ou Contributor)
        if isinstance(obj, Project):
            project = obj
        elif hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        else:
            return False

        # Vérifie si l'utilisateur est bien enregistré comme contributeur sur ce projet
        return Contributor.objects.filter(
            project=project, user=request.user
        ).exists()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée :
    - Les membres/contributeurs du projet ont un accès en lecture (GET, HEAD, OPTIONS).
    - Seul l'auteur de la ressource a le droit de modifier ou supprimer (PUT, PATCH, DELETE).
    """

    def has_object_permission(self, request, view, obj):
        # Accès autorisé pour les requêtes en lecture seule
        if request.method in permissions.SAFE_METHODS:
            return True

        # Pour la modification ou la suppression, l'utilisateur doit être l'auteur
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'project'):
            return obj.project.author == request.user

        return False