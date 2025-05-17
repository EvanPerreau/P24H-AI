"""
Module contenant la classe Action qui encapsule toutes les commandes et demandes disponibles dans le jeu.
"""
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple

from ..models.joueur import Joueur
from ..models.monstre import Monstre
from ..models.pioche import Pioche, TypeCarte
from .logger import Logger


class CommandType(Enum):
    """
    Types de commandes disponibles dans le jeu.
    """
    # Notifications serveur
    DEBUT_TOUR = "DEBUT_TOUR"
    FIN = "FIN"
    
    # Actions joueur
    PIOCHER = "PIOCHER"
    UTILISER = "UTILISER"
    ATTAQUER = "ATTAQUER"
    
    # Demandes d'information
    JOUEURS = "JOUEURS"
    MOI = "MOI"
    MONSTRES = "MONSTRES"
    PIOCHES = "PIOCHES"
    DAMAGE = "DAMAGE"


class Action:
    """
    Classe qui encapsule toutes les commandes et demandes disponibles dans le jeu.
    Permet de formater les commandes, les envoyer au serveur, et d'analyser les réponses.
    """
    
    def __init__(self, connection=None):
        """
        Initialise une instance d'Action avec une connexion.
        
        Args:
            connection: Instance de Connection à utiliser (optionnel)
        """
        self._connection = connection
    
    def set_connection(self, connection):
        """
        Définit l'instance de connexion à utiliser pour l'envoi/réception.
        
        Args:
            connection: Instance de Connection à utiliser
        """
        self._connection = connection
    
    def format_command(self, command: str, args: List[Any] = None) -> str:
        """
        Formate une commande pour l'envoi au serveur.
        
        Args:
            command: Le nom de la commande
            args: Les arguments de la commande (optionnel)
            
        Returns:
            str: La commande formatée
        """
        args = [str(arg) for arg in args if arg is not None]
        return "|".join([command] + args)
    
    def parse_response(self, response: str) -> List[str]:
        """
        Analyse une réponse du serveur.
        
        Args:
            response: La réponse du serveur
            
        Returns:
            Tuple[bool, str, List[str]]: Un tuple contenant (succès, message, parties de la réponse)
        """
        return response.strip().split('|')
    
    # ===== ACTIONS =====

    def send_team_name(self, team_name: str) -> int:
        """
        Génère une commande pour envoyer le nom de l'équipe.
        
        Args:
            team_name: Le nom de l'équipe

        Returns:
            team number
        """
        self._connection.send_message(team_name)
        return self.parse_response(self._connection.receive_message())[1]
        
    
    def piocher(self, expedition_number: int, malus_player_number: Optional[int] = None) -> bool:
        """
        Génère une commande pour piocher une carte.
        
        Args:
            expedition_number: Numéro de l'expédition (entre 0 et 5)
            malus_player_number: Numéro du joueur sur lequel appliquer le malus (entre 0 et 3, optionnel)
            
        Returns:
            bool: True si la commande a été envoyée avec succès, False sinon
        """
        
        self._connection.send_message(self.format_command(CommandType.PIOCHER.value, [expedition_number, malus_player_number]))
        
        return self.parse_response(self._connection.receive_message())[0] == "OK"
    
    def utiliser(self, type_carte: TypeCarte) -> bool:
        """
        Génère une commande pour utiliser une carte.
        
        Args:
            type_carte: Type de carte à utiliser (DEFENSE, ATTAQUE ou SAVOIR)
            
        Returns:
            bool: True si la commande a été envoyée avec succès, False sinon
        """
        
        self._connection.send_message(self.format_command(CommandType.UTILISER.value, [type_carte.value]))
        
        return self.parse_response(self._connection.receive_message())[0] == "OK"
    
    def attaquer(self, monster_number: int) -> bool:
        """
        Génère une commande pour attaquer un monstre.
        
        Args:
            monster_number: Numéro du monstre à attaquer (entre 0 et 2)
            
        Returns:
            bool: True si la commande a été envoyée avec succès, False sinon
        """
        
        self._connection.send_message(self.format_command(CommandType.ATTAQUER.value, [str(monster_number)]))
        
        return self.parse_response(self._connection.receive_message())[0] == "OK"
    
    # ===== DEMANDES D'INFORMATIONS =====
    
    def get_joueurs(self) -> List[Joueur]:
        """
        Génère une demande pour obtenir des informations sur tous les joueurs.
        
        Returns:
            Dict[str, Any]: Demande formatée
        """
        
        self._connection.send_message(self.format_command(CommandType.JOUEURS.value))
        
        return Joueur.from_server_response(self.parse_response(self._connection.receive_message()))
    
    def get_moi(self) -> Joueur:
        """
        Génère une demande pour obtenir des informations sur le joueur actuel.
        
        Returns:
            Dict[str, Any]: Demande formatée
        """
        
        self._connection.send_message(self.format_command(CommandType.MOI.value))
        
        return Joueur.from_server_response(self.parse_response(self._connection.receive_message()))
    
    def get_monstres(self) -> List[Monstre]:
        """
        Génère une demande pour obtenir des informations sur les monstres.
        
        Returns:
            Dict[str, Any]: Demande formatée
        """
        
        self._connection.send_message(self.format_command(CommandType.MONSTRES.value))
        
        return Monstre.from_server_response(self.parse_response(self._connection.receive_message()))
    
    def get_pioches(self) -> List[Pioche]:
        """
        Génère une demande pour obtenir des informations sur les expéditions.
        
        Returns:
            Dict[str, Any]: Demande formatée
        """
        
        self._connection.send_message(self.format_command(CommandType.PIOCHES.value))
        
        return Pioche.from_server_response(self.parse_response(self._connection.receive_message()))

    def get_damage(self) -> int:
        """
        Génère une demande pour obtenir des informations sur les dommages.
        
        Returns:
            Dict[str, Any]: Demande formatée
        """
        
        self._connection.send_message(self.format_command(CommandType.DAMAGE.value))
        
        return int(self.parse_response(self._connection.receive_message())[1])
