#!/usr/bin/env python
"""Utilitaire en ligne de commande de Django pour les tâches administratives."""
import os
import sys


def main():
    """Exécute les tâches d'administration (migrations, serveur de dev, tests, etc.)."""
    # Définit le fichier de configuration par défaut du projet Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk.settings')
    try:
        # Importation dynamique de l'exécuteur de commandes de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Message d'erreur explicite si l'environnement virtuel n'est pas activé ou si Django n'est pas installé
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Transmet les arguments de la ligne de commande (sys.argv) à l'utilitaire de Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Point d'entrée principal de l'exécution du script
    main()