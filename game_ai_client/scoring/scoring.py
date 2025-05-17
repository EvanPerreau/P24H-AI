from ..models import Monstre
from ..models import Pioche
from ..models import Joueur
from ..models import TypeCarte
from ..models import Deck

class Scoring:
    def __init__(self, monstres: list[Monstre], cartes: list[Pioche], me: Joueur, deck: Deck, fdr: int, nb_tours: int):
        """
        Initialise le système de scoring pour le jeu.

        Args:
            monstres: Liste d'instances de la classe Monstre
            Pioche: Instance de la classe Pioche
        """
        self.monstres = monstres
        self.cartes = cartes
        self.me = me
        self.fdr = fdr
        self.deck = deck
        self.nb_tours = nb_tours
        self.scored_monstres = []
        self.scored_cartes = []
        self.set_score_monstres()
        self.set_score_cartes()

    def get_scored_monstres(self):
        """
        Retourne la liste des monstres avec leurs scores.

        Returns:
            list: Liste de dictionnaires contenant l'index et le score des monstres
        """
        return self.scored_monstres
    
    def get_scored_cartes(self):
        """
        Retourne la liste des cartes avec leurs scores.

        Returns:
            list: Liste de dictionnaires contenant l'index et le score des cartes
        """
        return self.scored_cartes

    def set_score_monstres(self):
        """
        Définit le score du monstre.

        Args:
            monstre: Instance de la classe Monstre
        """
        for monstre in self.monstres:
            vie_max = monstre.gain_savoir / 4
            multiplicateur_vie_restante = (((monstre.vie - 1) / (vie_max -1)) * 0.5 - 1) * -1

            multiplicateur_monstre_oneshot = 1
            if (self.me.score_attaque + self.deck.sum_values_by_type(TypeCarte.ATTAQUE)) >= monstre.vie:
                multiplicateur_monstre_oneshot = 1.5

            score = (monstre.gain_savoir * self.get_monstres_multiplicateurs()) * multiplicateur_vie_restante * multiplicateur_monstre_oneshot
            
            self.scored_monstres.append({
                "index": monstre.index,
                "score": score
            })

    def set_score_cartes(self):
        """
        Définit le score des cartes.

        Args:
            carte: Instance de la classe Pioche
        """
        for carte in self.cartes:

            score_valeur = 0

            if carte.type_carte == TypeCarte.DEFENSE:
                multiplicateur_fdr = 1
                if self.fdr > (self.me.score_defense + self.deck.sum_values_by_type(TypeCarte.DEFENSE)):
                    defense = self.fdr - (self.me.score_defense + self.deck.sum_values_by_type(TypeCarte.DEFENSE))
                    multiplicateur_fdr = (1 + defense) / 10

                multiplicateur_hard_danger = 1
                if self.fdr > (self.me.score_defense + self.deck.sum_values_by_type(TypeCarte.DEFENSE)) + self.me.vie:
                    multiplicateur_hard_danger = 100

                score_valeur = carte.valeur * multiplicateur_fdr * multiplicateur_hard_danger * 2

            elif carte.type_carte == TypeCarte.ATTAQUE:
                multiplicateur_no_attaque = 1
                if (self.me.score_attaque + self.deck.sum_values_by_type(TypeCarte.ATTAQUE)) == 0:
                    multiplicateur_no_attaque = 5
                
                multiplicateur_no_monstre = 1
                if self.scored_monstres.__len__() == 0:
                    multiplicateur_no_monstre = 0

                score_monstre_max = 0
                for monstre in self.scored_monstres:
                    if monstre["score"] > score_monstre_max:
                        score_monstre_max = monstre["score"]/10
                    
                if score_monstre_max == 0:
                    score_monstre_max = 1

                score_valeur = carte.valeur * multiplicateur_no_attaque * multiplicateur_no_monstre * score_monstre_max
                
            elif carte.type_carte == TypeCarte.SAVOIR:
                multiplicateur_no_monstre = 1
                if self.scored_monstres.__len__() == 0:
                    multiplicateur_no_monstre = 5
                else:
                    multiplicateur_no_monstre = 1/self.scored_monstres.__len__()

                score_valeur = carte.valeur * multiplicateur_no_monstre

            self.scored_cartes.append({
                "index": carte.index,
                "score": score_valeur
            })
    
    def get_monstres_multiplicateurs(self):
        # TODO: Dans (16 - self.nb_tours) * 2 * 4, 4 correspond aun ombre de joueur vivant
        if (16 - self.nb_tours) * 2 * 4 < self.monstres[0].gain_savoir / 4:
            return 0
        elif self.monstres[0].gain_savoir / 4 < 40:
            return 4
        elif self.monstres[0].gain_savoir / 4 < 110:
            return 2
        else:
            return 0