from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# On importe RegisterView (le nom exact présent dans ta vue d'authentification)
from authentication.views import RegisterView
from projects.views import (
    CommentViewSet,
    ContributorViewSet,
    IssueViewSet,
    ProjectViewSet,
)

# 1. Router principal pour les projets (/api/projects/)
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

# 2. Router imbriqué pour les contributeurs et les tickets
# URLs générées : /api/projects/{project_pk}/users/ et /api/projects/{project_pk}/issues/
projects_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project'
)
projects_router.register(
    r'users', ContributorViewSet, basename='project-users'
)
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

# 3. Router imbriqué pour les commentaires
# URL générée : /api/projects/{project_pk}/issues/{issue_pk}/comments/
issues_router = routers.NestedSimpleRouter(
    projects_router, r'issues', lookup='issue'
)
issues_router.register(
    r'comments', CommentViewSet, basename='issue-comments'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inscription de l'utilisateur
    path('api/signup/', RegisterView.as_view(), name='signup'),
    # Connexion JWT : Récupération des tokens (access + refresh)
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    # Rafraîchissement du token access
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Inclusion des URLs du router DRF
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(issues_router.urls)),
]