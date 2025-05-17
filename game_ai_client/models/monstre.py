"""
Module contenant la classe pour représenter un monstre dans le jeu.
"""
from typing import List
from ..utils.logger import Logger


class Monstre:
    """
    Classe représentant un monstre dans le jeu.
    Contient les informations sur la vie et le gain de savoir.
    """
    def __init__(self, vie: int = 0, gain_savoir: int = 0):
        """
        Initialise un monstre avec ses statistiques.
        
        Args:
            vie: Points de vie du monstre
            gain_savoir: Gain de savoir obtenu en battant le monstre
        """
        self.vie = vie
        self.gain_savoir = gain_savoir
        self.index = 0

    def set_index(self, index: int):
        """
        Définit l'index du monstre.
        
        Args:
            index: Index du monstre
        """
        self.index = index
    
    @classmethod
    def from_array(cls, data: List[str]) -> 'Monstre':
        """
        Crée un objet Monstre à partir d'un tableau de données.
        
        Args:
            data: Tableau de 2 éléments [Vie, GainSavoir]
            
        Returns:
            Monstre: Instance de Monstre avec les valeurs analysées
        """
        if len(data) != 2:
            Logger.warning(f"Format de données monstre invalide, taille attendue: 2, taille reçue: {len(data)}")
            return cls()
        
        try:
            return cls(
                vie=int(data[0]),
                gain_savoir=int(data[1])
            )
        except ValueError as e:
            Logger.warning(f"Erreur de conversion des données monstre: {e}")
            return cls()
    
    @classmethod
    def from_server_response(cls, data: List[str]) -> List['Monstre']:
        """
        Crée plusieurs monstres à partir d'un tableau plat de données.
        Chaque monstre occupe 2 éléments consécutifs dans le tableau.
        
        Args:
            data: Tableau contenant toutes les données des monstres à la suite
            
        Returns:
            List[Monstre]: Liste d'instances de Monstre
        """
        monstres = []
        nombre_elements_par_monstre = 2
        
        # Vérifier que le nombre d'éléments est un multiple du nombre d'éléments par monstre
        if len(data) % nombre_elements_par_monstre != 0:
            Logger.warning(f"Format de données monstres invalide: {len(data)} éléments n'est pas un multiple de {nombre_elements_par_monstre}")
        
        id = 0
        # Traiter les monstres par blocs de 2 éléments
        for i in range(0, len(data), nombre_elements_par_monstre):
            if i + nombre_elements_par_monstre <= len(data):
                monstre_data = data[i:i+nombre_elements_par_monstre]
                monstre = cls.from_array(monstre_data)
                monstre.set_index(id)
                monstres.append(monstre)
                id += 1
        
        return monstres
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle du monstre."""
        return f"Monstre(index={self.index}, vie={self.vie}, gain_savoir={self.gain_savoir})"
