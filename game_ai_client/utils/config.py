"""
Module de configuration pour le client IA du jeu.
Contient les paramètres de connexion au serveur et d'autres paramètres de configuration.
"""
from typing import Dict, Any


class Config:
    """
    Classe de configuration pour le client IA du jeu.
    Stocke les paramètres de connexion au serveur et d'autres paramètres de configuration.
    """
    # Paramètres de connexion au serveur
    HOSTNAME_SERVER: str = "localhost"
    PORT_SERVER: int = 8080
    
    # Paramètres de journalisation
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "game_client.log"
    
    # Des paramètres de jeu supplémentaires peuvent être ajoutés ici
    GAME_SETTINGS: Dict[str, Any] = {
        "timeout": 30,  # secondes
        "retry_attempts": 3,
    }
    
    @classmethod
    def get_server_address(cls) -> tuple:
        """
        Renvoie l'adresse du serveur sous forme de tuple (nom d'hôte, port).
        
        Returns:
            tuple: Un tuple contenant le nom d'hôte et le port
        """
        return (cls.HOSTNAME_SERVER, cls.PORT_SERVER)
