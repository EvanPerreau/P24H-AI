"""
Point d'entrée principal pour le client IA du jeu.
Démontre comment utiliser le client pour se connecter à un serveur de jeu et exécuter l'IA.
"""
import argparse
import sys
from typing import Dict, Any

from game_ai_client import AIClient
from game_ai_client.utils import Config, Logger, LogLevel


def parse_arguments() -> Dict[str, Any]:
    """
    Analyse les arguments de ligne de commande.
    
    Returns:
        Dict[str, Any]: Dictionnaire des arguments analysés
    """
    parser = argparse.ArgumentParser(description='Client IA du jeu')
    
    parser.add_argument(
        '--host',
        type=str,
        default=Config.HOSTNAME_SERVER,
        help=f'Nom d\'hôte du serveur (par défaut: {Config.HOSTNAME_SERVER})'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=Config.PORT_SERVER,
        help=f'Port du serveur (par défaut: {Config.PORT_SERVER})'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'ACTION', 'WARNING', 'ERROR', 'CRITICAL'],
        default=Config.LOG_LEVEL,
        help=f'Niveau de journalisation (par défaut: {Config.LOG_LEVEL})'
    )
    
    args = parser.parse_args()
    return vars(args)


def configure_from_args(args: Dict[str, Any]):
    """
    Configure l'application à partir des arguments de ligne de commande.
    
    Args:
        args: Dictionnaire des arguments analysés
    """
    # Mettre à jour la configuration
    Config.HOSTNAME_SERVER = args['host']
    Config.PORT_SERVER = args['port']
    Config.LOG_LEVEL = args['log_level']
    
    Logger.info(f"Configuré avec hôte={Config.HOSTNAME_SERVER}, port={Config.PORT_SERVER}")


def main():
    """
    Point d'entrée principal pour l'application.
    """
    # Analyser les arguments de ligne de commande
    args = parse_arguments()
    
    # Configurer l'application
    configure_from_args(args)
    
    try:
        # Démarrer le client IA directement via la méthode de classe
        AIClient.start()
    except KeyboardInterrupt:
        Logger.info("Application terminée par l'utilisateur")
    except Exception as e:
        Logger.critical(f"Erreur d'application: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
