"""
Module contenant la classe pour représenter un joueur dans le jeu.
"""
from typing import List
from ..utils.logger import Logger


class Joueur:
    """
    Classe représentant un joueur dans le jeu.
    Contient les informations sur la vie et les scores.
    """
    def __init__(self, vie: int = 0, score_defense: int = 0, score_attaque: int = 0, score_savoir: int = 0):
        """
        Initialise un joueur avec ses statistiques.
        
        Args:
            vie: Points de vie du joueur
            score_defense: Score de défense du joueur
            score_attaque: Score d'attaque du joueur
            score_savoir: Score de savoir du joueur
        """
        self.vie = vie
        self.score_defense = score_defense
        self.score_attaque = score_attaque
        self.score_savoir = score_savoir
    
    @classmethod
    def from_array(cls, data: List[str]) -> 'Joueur':
        """
        Crée un objet Joueur à partir d'un tableau de données.
        
        Args:
            data: Tableau de 4 éléments [Vie, ScoreDefense, ScoreAttaque, ScoreSavoir]
            
        Returns:
            Joueur: Instance de Joueur avec les valeurs analysées
        """
        if len(data) != 4:
            Logger.warning(f"Format de données joueur invalide, taille attendue: 4, taille reçue: {len(data)}")
            return cls()
        
        try:
            return cls(
                vie=int(data[0]),
                score_defense=int(data[1]),
                score_attaque=int(data[2]),
                score_savoir=int(data[3])
            )
        except ValueError as e:
            Logger.warning(f"Erreur de conversion des données joueur: {e}")
            return cls()
    
    @classmethod
    def from_server_response(cls, data: List[str]) -> List['Joueur']:
        """
        Crée plusieurs joueurs à partir d'un tableau plat de données.
        Chaque joueur occupe 4 éléments consécutifs dans le tableau.
        
        Args:
            data: Tableau contenant toutes les données des joueurs à la suite
            
        Returns:
            List[Joueur]: Liste d'instances de Joueur
        """
        joueurs = []
        nombre_elements_par_joueur = 4
        
        # Vérifier que le nombre d'éléments est un multiple du nombre d'éléments par joueur
        if len(data) % nombre_elements_par_joueur != 0:
            Logger.warning(f"Format de données joueurs invalide: {len(data)} éléments n'est pas un multiple de {nombre_elements_par_joueur}")
        
        # Traiter les joueurs par blocs de 4 éléments
        for i in range(0, len(data), nombre_elements_par_joueur):
            if i + nombre_elements_par_joueur <= len(data):
                joueur_data = data[i:i+nombre_elements_par_joueur]
                joueur = cls.from_array(joueur_data)
                joueurs.append(joueur)
        
        return joueurs
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle du joueur."""
        return f"Joueur(vie={self.vie}, defense={self.score_defense}, attaque={self.score_attaque}, savoir={self.score_savoir})"
