"""
Django management command pour générer les données de test
Utilisation: poetry run python manage.py create_test_data
"""

from django.core.management.base import BaseCommand
from authentication.models import User
from projects.models import Project, Contributor, Issue, Comment


class Command(BaseCommand):
    help = "Crée des données de test pour la SoftDesk API"

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(
            self.style.SUCCESS("Création des données de test pour SoftDesk API")
        )
        self.stdout.write("=" * 60)

        # 1. Créer les utilisateurs
        self.stdout.write("\n📝 Création des utilisateurs...")

        user1, created = User.objects.get_or_create(
            username="alice",
            defaults={
                "email": "alice@softdesk.com",
                "first_name": "Alice",
                "last_name": "Dupont",
                "birth_date": "2000-05-15",
                "can_be_contacted": True,
                "can_data_be_shared": False,
            },
        )
        if created:
            user1.set_password("Alice123!")
            user1.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur créé: {user1.username}")
            )
        else:
            self.stdout.write(f"⏭️  Utilisateur existe déjà: {user1.username}")

        user2, created = User.objects.get_or_create(
            username="bob",
            defaults={
                "email": "bob@softdesk.com",
                "first_name": "Bob",
                "last_name": "Martin",
                "birth_date": "1998-10-20",
                "can_be_contacted": True,
                "can_data_be_shared": True,
            },
        )
        if created:
            user2.set_password("Bob123!")
            user2.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur créé: {user2.username}")
            )
        else:
            self.stdout.write(f"⏭️  Utilisateur existe déjà: {user2.username}")

        user3, created = User.objects.get_or_create(
            username="charlie",
            defaults={
                "email": "charlie@softdesk.com",
                "first_name": "Charlie",
                "last_name": "Bernard",
                "birth_date": "2001-03-10",
                "can_be_contacted": False,
                "can_data_be_shared": True,
            },
        )
        if created:
            user3.set_password("Charlie123!")
            user3.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur créé: {user3.username}")
            )
        else:
            self.stdout.write(f"⏭️  Utilisateur existe déjà: {user3.username}")

        # 2. Créer les projets
        self.stdout.write("\n🏗️  Création des projets...")

        project1, created = Project.objects.get_or_create(
            name="Backend API SoftDesk",
            defaults={
                "description": "Développement du backend REST API pour la plateforme SoftDesk",
                "type": "BACKEND",
                "author": user1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Projet créé: {project1.name}"))
        else:
            self.stdout.write(f"⏭️  Projet existe déjà: {project1.name}")

        project2, created = Project.objects.get_or_create(
            name="Frontend Web Application",
            defaults={
                "description": "Interface web pour la gestion des projets et tickets",
                "type": "FRONTEND",
                "author": user2,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Projet créé: {project2.name}"))
        else:
            self.stdout.write(f"⏭️  Projet existe déjà: {project2.name}")

        # 3. Ajouter les contributeurs
        self.stdout.write("\n👥 Ajout des contributeurs aux projets...")

        contrib1, created = Contributor.objects.get_or_create(
            user=user1,
            project=project1,
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ {user1.username} ajouté à {project1.name}")
            )

        contrib2, created = Contributor.objects.get_or_create(
            user=user1,
            project=project2,
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ {user1.username} ajouté à {project2.name}")
            )

        contrib3, created = Contributor.objects.get_or_create(
            user=user2,
            project=project2,
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ {user2.username} ajouté à {project2.name}")
            )

        contrib4, created = Contributor.objects.get_or_create(
            user=user3,
            project=project1,
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ {user3.username} ajouté à {project1.name}")
            )

        # 4. Créer les issues
        self.stdout.write("\n🎫 Création des issues...")

        issue1, created = Issue.objects.get_or_create(
            title="Implémenter l'authentification JWT",
            defaults={
                "description": "Ajouter la gestion de l'authentification JWT avec django-rest-framework-simplejwt",
                "priority": "HIGH",
                "tag": "FEATURE",
                "status": "IN_PROGRESS",
                "project": project1,
                "author": user1,
                "assigned_to": user3,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Issue créée: {issue1.title}"))
        else:
            self.stdout.write(f"⏭️  Issue existe déjà: {issue1.title}")

        issue2, created = Issue.objects.get_or_create(
            title="Problème de performance sur les listes",
            defaults={
                "description": "Les listes de projets chargent lentement avec plus de 100 éléments",
                "priority": "MEDIUM",
                "tag": "BUG",
                "status": "TO_DO",
                "project": project1,
                "author": user3,
                "assigned_to": user1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Issue créée: {issue2.title}"))
        else:
            self.stdout.write(f"⏭️  Issue existe déjà: {issue2.title}")

        issue3, created = Issue.objects.get_or_create(
            title="Ajouter pagination aux endpoints",
            defaults={
                "description": "Implémenter la pagination pour respecter les principes du Green Code",
                "priority": "MEDIUM",
                "tag": "FEATURE",
                "status": "FINISHED",
                "project": project1,
                "author": user1,
                "assigned_to": None,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Issue créée: {issue3.title}"))
        else:
            self.stdout.write(f"⏭️  Issue existe déjà: {issue3.title}")

        issue4, created = Issue.objects.get_or_create(
            title="Design de l'interface utilisateur",
            defaults={
                "description": "Créer les maquettes et le design system pour la frontend",
                "priority": "HIGH",
                "tag": "TASK",
                "status": "IN_PROGRESS",
                "project": project2,
                "author": user2,
                "assigned_to": user1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Issue créée: {issue4.title}"))
        else:
            self.stdout.write(f"⏭️  Issue existe déjà: {issue4.title}")

        # 5. Créer les commentaires
        self.stdout.write("\n💬 Création des commentaires...")

        comment1, created = Comment.objects.get_or_create(
            uuid="12345678-1234-5678-1234-567812345678",
            defaults={
                "description": "Excellente idée ! J'ai déjà commencé la mise en œuvre.",
                "issue": issue1,
                "author": user3,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Commentaire créé sur: {issue1.title}")
            )
        else:
            self.stdout.write(f"⏭️  Commentaire existe déjà")

        comment2, created = Comment.objects.get_or_create(
            uuid="87654321-4321-8765-4321-876543218765",
            defaults={
                "description": "Trouvé le problème ! C'est un problème de N+1 queries.",
                "issue": issue2,
                "author": user1,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Commentaire créé sur: {issue2.title}")
            )
        else:
            self.stdout.write(f"⏭️  Commentaire existe déjà")

        comment3, created = Comment.objects.get_or_create(
            uuid="11111111-2222-3333-4444-555555555555",
            defaults={
                "description": "Merci pour la correction ! Les performances sont maintenant bien meilleures.",
                "issue": issue2,
                "author": user3,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Commentaire créé sur: {issue2.title}")
            )
        else:
            self.stdout.write(f"⏭️  Commentaire existe déjà")

        comment4, created = Comment.objects.get_or_create(
            uuid="99999999-8888-7777-6666-555555555555",
            defaults={
                "description": "La pagination est maintenant active et fonctionne parfaitement !",
                "issue": issue3,
                "author": user1,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Commentaire créé sur: {issue3.title}")
            )
        else:
            self.stdout.write(f"⏭️  Commentaire existe déjà")

        comment5, created = Comment.objects.get_or_create(
            uuid="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            defaults={
                "description": "Le design commence à prendre forme. Rendez-vous jeudi pour la révision ?",
                "issue": issue4,
                "author": user2,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Commentaire créé sur: {issue4.title}")
            )
        else:
            self.stdout.write(f"⏭️  Commentaire existe déjà")

        # Afficher les statistiques
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("📊 STATISTIQUES DES DONNÉES DE TEST"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"👤 Utilisateurs: {User.objects.count()}")
        self.stdout.write(f"📂 Projets: {Project.objects.count()}")
        self.stdout.write(f"👥 Contributeurs: {Contributor.objects.count()}")
        self.stdout.write(f"🎫 Issues: {Issue.objects.count()}")
        self.stdout.write(f"💬 Commentaires: {Comment.objects.count()}")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ Données de test créées avec succès !"))
        self.stdout.write("=" * 60)
        self.stdout.write("\n📝 Identifiants pour les tests :")
        self.stdout.write("   Utilisateur 1: alice / Alice123!")
        self.stdout.write("   Utilisateur 2: bob / Bob123!")
        self.stdout.write("   Utilisateur 3: charlie / Charlie123!")
        self.stdout.write("\n🌐 API disponible sur: http://127.0.0.1:8000/")
        self.stdout.write(
            "📚 Documentation API: http://127.0.0.1:8000/ (page d'accueil DRF)"
        )
        self.stdout.write("\n💡 Premiers pas :")
        self.stdout.write("   1. POST /api/signup/ pour créer un nouvel utilisateur")
        self.stdout.write("   2. POST /api/login/ pour obtenir les tokens JWT")
        self.stdout.write("   3. GET /api/projects/ pour lister les projets")
        self.stdout.write("   4. Voir README.md pour tous les endpoints disponibles")
        self.stdout.write("=" * 60 + "\n")
