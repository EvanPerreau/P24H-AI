"""
Module client IA pour le jeu.
Gère la logique du jeu et la prise de décision basée sur la communication avec le serveur.
"""
from typing import Dict, Any, List

from .connection import Connection
from .utils.logger import Logger
from .utils.action import Action
from .models.deck import Deck
from .scoring.scoring import Scoring
from .models import TypeCarte


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
        self.action = Action(self.connection)
        self.game_state: List[str] = []
        self.team_number: int = None
        self.deck = Deck()
        Logger.info("Client IA initialisé")
  
    def __init__(self):
        """
        Initialise le client IA si ce n'est pas déjà fait.
        """
        if not hasattr(self, 'game_state'):
            self._initialize()
    
    def process_message(self, message: str) -> List[str]:
        """
        Traite un message reçu du serveur au format "NomCommande|Argument1|Argument2".
        
        Args:
            message: Le message à traiter
            
        Returns:
            List[str]: Le message analysé sous forme de liste
        """
        return message.strip().split('|')
    
    def update_game_state(self, state_update: List[str]):
        """
        Met à jour l'état du jeu avec de nouvelles informations.
        
        Args:
            state_update: Les nouvelles informations d'état
        """
        self.game_state = state_update
        Logger.debug(f"État du jeu mis à jour: {self.game_state}")
    
    def make_decision(self):
        """
        Prend une décision basée sur l'état actuel du jeu.
        C'est ici que la logique de l'IA serait implémentée.
        
        Returns:
            Dict[str, Any]: La décision prise par l'IA
        """
        # Espace réservé pour la logique de décision de l'IA
        # Ceci devrait être implémenté en fonction des règles spécifiques du jeu
        Logger.info("Prise de décision basée sur l'état actuel du jeu")

        if self.game_state[0] == "NOM_EQUIPE":
            self.team_number = self.action.send_team_name("BUTiChat")

        if self.game_state[0] == "DEBUT_TOUR":
            me = self.action.get_moi()
            other_players = [player for player in self.action.get_joueurs() if int(player.index) != int(self.team_number)]
            monstres = self.action.get_monstres()
            pioches = self.action.get_pioches()
            degats = self.action.get_degats()
            scoring = Scoring(monstres, pioches, me, self.deck, degats)
            if (int(self.game_state[2]) + 1) % 4 != 0:
                card = scoring.get_scored_cartes()[0]
                for scored_carte in scoring.get_scored_cartes():
                    if scored_carte["score"] > card["score"]:
                        card = scored_carte
                
                self.action.piocher(card["index"])
                for p in pioches:
                    if p.index == card["index"]:
                        self.deck.add_card(p)
            
            elif self.deck.sum_values_by_type(TypeCarte.ATTAQUE) <= 0 and me.score_attaque <= 0:
                card = scoring.get_scored_cartes()[0]
                for scored_carte in scoring.get_scored_cartes():
                    if scored_carte["score"] > card["score"]:
                        card = scored_carte
                
                self.action.piocher(card["index"])
                for p in pioches:
                    if p.index == card["index"]:
                        self.deck.add_card(p)
                        break

            else:
                self.action.utiliser(TypeCarte.ATTAQUE)
                monster = scoring.get_scored_monstres()[0]
                for scored_monster in scoring.get_scored_monstres():
                    if scored_monster["score"] > monster["score"]:
                        monster = scored_monster
                
                self.action.attaquer(monster["index"])

            if int(self.game_state[2]) + 1 == 16:
                self.action.utiliser(TypeCarte.DEFENSE)
                self.action.utiliser(TypeCarte.SAVOIR)

            
    
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

                if parsed_message[0] == "FIN":
                    break
                
                # Mettre à jour l'état du jeu
                self.update_game_state(parsed_message)

                Logger.info(f"État du jeu mis à jour: {self.game_state}")
                
                # Prendre une décision
                self.make_decision()
                
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
