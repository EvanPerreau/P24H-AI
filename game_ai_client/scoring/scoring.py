from ..models import Monstre
from ..models import Pioche

class Scoring:
    def __init__(self, monstres: list[Monstre], cartes: list[Pioche]):
        """
        Initialise le système de scoring pour le jeu.

        Args:
            monstres: Liste d'instances de la classe Monstre
            Pioche: Instance de la classe Pioche
        """
        self.monstres = monstres
        self.cartes = cartes

    