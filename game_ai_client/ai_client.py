"""
Module client IA pour le jeu.
Gère la logique du jeu et la prise de décision basée sur la communication avec le serveur.
"""
from typing import Dict, Any, Optional
import json

from .connection import Connection
from .utils.logger import Logger, LogLevel


class AIClient:
    """
    Client IA pour le jeu.
    Gère la logique du jeu et la prise de décision basée sur la communication avec le serveur.
    """
    # Instance singleton
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        Implémente le modèle singleton.
        """
        if cls._instance is None:
            cls._instance = super(AIClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """
        Initialise le client IA.
        """
        self.connection = Connection.get_instance()
        self.game_state: Dict[str, Any] = {}
        Logger.info("Client IA initialisé")
  
    def __init__(self):
        """
        Initialise le client IA si ce n'est pas déjà fait.
        """
        if not hasattr(self, 'game_state'):
            self._initialize()
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Traite un message reçu du serveur.
        
        Args:
            message: Le message à traiter
            
        Returns:
            Dict[str, Any]: Le message analysé sous forme de dictionnaire
        """
        try:
            parsed_message = json.loads(message)
            Logger.debug(f"Message traité: {parsed_message}")
            return parsed_message
        except json.JSONDecodeError:
            Logger.warning(f"Échec de l'analyse du message JSON: {message}")
            return {"raw": message}
    
    def update_game_state(self, state_update: Dict[str, Any]):
        """
        Met à jour l'état du jeu avec de nouvelles informations.
        
        Args:
            state_update: Les nouvelles informations d'état
        """
        self.game_state.update(state_update)
        Logger.debug(f"État du jeu mis à jour: {self.game_state}")
    
    def make_decision(self) -> Dict[str, Any]:
        """
        Prend une décision basée sur l'état actuel du jeu.
        C'est ici que la logique de l'IA serait implémentée.
        
        Returns:
            Dict[str, Any]: La décision prise par l'IA
        """
        # Espace réservé pour la logique de décision de l'IA
        # Ceci devrait être implémenté en fonction des règles spécifiques du jeu
        Logger.info("Prise de décision basée sur l'état actuel du jeu")
        
        # Exemple simple de décision
        decision = {
            "action": "move",
            "parameters": {
                "direction": "forward",
                "steps": 1
            }
        }
        
        return decision
    
    def send_decision(self, decision: Dict[str, Any]):
        """
        Envoie une décision au serveur.
        
        Args:
            decision: La décision à envoyer
        """
        message = json.dumps(decision)
        self.connection.send_message(message)
    
    def run_game_loop(self):
        """
        Exécute la boucle principale du jeu.
        Reçoit continuellement des messages, met à jour l'état du jeu, prend des décisions et envoie des réponses.
        """
        Logger.info("Démarrage de la boucle de jeu")
        try:
            while True:
                # Recevoir un message du serveur
                message = self.connection.receive_message()
                
                # Traiter le message
                parsed_message = self.process_message(message)
                
                # Vérifier si le jeu est terminé
                if parsed_message.get("game_over", False):
                    Logger.info(f"Jeu terminé. Résultat: {parsed_message.get('result', 'inconnu')}")
                    break
                
                # Mettre à jour l'état du jeu
                self.update_game_state(parsed_message)
                
                # Prendre une décision
                decision = self.make_decision()
                
                # Envoyer la décision au serveur
                self.send_decision(decision)
                
        except ConnectionError as e:
            Logger.error(f"Erreur de connexion: {e}")
        except Exception as e:
            Logger.critical(f"Erreur inattendue: {e}")
        finally:
            self.connection.stop()
            Logger.info("Boucle de jeu terminée")
    
    @classmethod
    def start(cls):
        """
        Démarre le client IA.
        """
        instance = cls()
        Logger.info("Démarrage du client IA")
        instance.run_game_loop()
