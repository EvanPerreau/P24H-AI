"""
Module contenant les classes pour représenter une pioche et les types de cartes dans le jeu.
"""
from enum import Enum
from typing import List, Optional
from ..utils.logger import Logger


class TypeCarte(Enum):
    """
    Enumération des types de cartes disponibles dans le jeu.
    """
    DEFENSE = "DEFENSE"
    ATTAQUE = "ATTAQUE"
    SAVOIR = "SAVOIR"


class Pioche:
    """
    Classe représentant une pioche (expédition) dans le jeu.
    Contient les informations sur le type de carte et sa valeur.
    """
    def __init__(self, type_carte: Optional[TypeCarte] = None, valeur: int = 0):
        """
        Initialise une pioche avec son type et sa valeur.
        
        Args:
            type_carte: Type de carte (DEFENSE, ATTAQUE ou SAVOIR)
            valeur: Valeur numérique de la carte
        """
        self.type_carte = type_carte
        self.valeur = valeur
        self.index = 0

    def set_index(self, index: int):
        """
        Définit l'index de la pioche.
        
        Args:
            index: Index de la pioche
        """
        self.index = index
    
    @classmethod
    def from_array(cls, data: List[str]) -> 'Pioche':
        """
        Crée un objet Pioche à partir d'un tableau de données.
        
        Args:
            data: Tableau de 2 éléments [Type, Valeur]
            
        Returns:
            Pioche: Instance de Pioche avec les valeurs analysées
        """
        if len(data) != 2:
            Logger.warning(f"Format de données pioche invalide, taille attendue: 2, taille reçue: {len(data)}")
            return cls()
        
        try:
            type_carte = None
            if data[0] in [t.value for t in TypeCarte]:
                type_carte = TypeCarte(data[0])
            
            return cls(
                type_carte=type_carte,
                valeur=int(data[1])
            )
        except (ValueError, KeyError) as e:
            Logger.warning(f"Erreur de conversion des données pioche: {e}")
            return cls()
    
    @classmethod
    def from_server_response(cls, data: List[str]) -> List['Pioche']:
        """
        Crée plusieurs pioches à partir d'un tableau plat de données.
        Chaque pioche occupe 2 éléments consécutifs dans le tableau.
        
        Args:
            data: Tableau contenant toutes les données des pioches à la suite
            
        Returns:
            List[Pioche]: Liste d'instances de Pioche
        """
        pioches = []
        nombre_elements_par_pioche = 2
        
        # Vérifier que le nombre d'éléments est un multiple du nombre d'éléments par pioche
        if len(data) % nombre_elements_par_pioche != 0:
            Logger.warning(f"Format de données pioches invalide: {len(data)} éléments n'est pas un multiple de {nombre_elements_par_pioche}")
        
        id = 0
        # Traiter les pioches par blocs de 2 éléments
        for i in range(0, len(data), nombre_elements_par_pioche):
            if i + nombre_elements_par_pioche <= len(data):
                pioche_data = data[i:i+nombre_elements_par_pioche]
                pioche = cls.from_array(pioche_data)
                pioche.set_index(id)
                pioches.append(pioche)
                id += 1
        
        return pioches
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle de la pioche."""
        type_str = self.type_carte.value if self.type_carte else "INCONNU"
        return f"Pioche(index={self.index}, type={type_str}, valeur={self.valeur})"
