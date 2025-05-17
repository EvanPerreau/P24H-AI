"""
Module contenant la classe Deck pour gérer les pioches organisées par type.
"""
from typing import Dict, List, Tuple
from collections import defaultdict

from .pioche import Pioche, TypeCarte
from ..utils.logger import Logger


class Deck:
    """
    Classe représentant un deck de cartes organisé par type.
    Permet de gérer et d'analyser les collections de pioches par type (DEFENSE, ATTAQUE, SAVOIR).
    """
    
    def __init__(self):
        """
        Initialise un deck vide avec des collections pour chaque type de carte.
        """
        self.collections: Dict[TypeCarte, List[Pioche]] = {
            TypeCarte.DEFENSE: [],
            TypeCarte.ATTAQUE: [],
            TypeCarte.SAVOIR: []
        }
    
    def add_card(self, pioche: Pioche):
        """
        Ajoute une seule pioche au deck.
        
        Args:
            pioche: Pioche à ajouter
            
        Returns:
            bool: True si la pioche a été ajoutée, False sinon
        """
        card_count = self.count_cards_by_type(pioche.type_carte)
        Logger.debug(f"Card count: {card_count}")
        Logger.debug(f"Card values: {self.sum_values_by_type(pioche.type_carte)}")
        Logger.debug(f"Card value: {pioche.valeur}")

        # Ajuster la valeur selon le nombre de cartes du même type
        if card_count > 8:
            pioche.valeur = int(pioche.valeur * 2)
        elif card_count >= 5:
            pioche.valeur = int(pioche.valeur * 1.5)

        self.collections[pioche.type_carte].append(pioche)
        Logger.debug(f"Card count: {self.count_cards_by_type(pioche.type_carte)}")
        Logger.debug(f"Card values: {self.sum_values_by_type(pioche.type_carte)}")

    def remove_cards_by_type(self, type_carte: TypeCarte):
        """
        Supprime toutes les pioches d'un type spécifique.
        
        Args:
            type_carte: Type de carte à supprimer
        """
        self.collections[type_carte] = []
    
    def count_cards_by_type(self, type_carte: TypeCarte) -> int:
        """
        Compte le nombre de pioches d'un type spécifique.
        
        Args:
            type_carte: Type de carte à compter
            
        Returns:
            int: Nombre de pioches du type spécifié
        """
        return len(self.collections.get(type_carte, []))
    
    def sum_values_by_type(self, type_carte: TypeCarte) -> int:
        """
        Calcule la somme des valeurs des pioches d'un type spécifique.
        
        Args:
            type_carte: Type de carte dont on veut la somme des valeurs
            
        Returns:
            int: Somme des valeurs des pioches du type spécifié
        """
        return sum(pioche.valeur for pioche in self.collections.get(type_carte, []))
    
    def get_summary(self) -> Dict[str, Tuple[int, int]]:
        """
        Génère un résumé du deck avec le nombre de cartes et la somme des valeurs par type.
        
        Returns:
            Dict[str, Tuple[int, int]]: Dictionnaire avec le type de carte comme clé 
                                        et un tuple (nombre, somme) comme valeur
        """
        summary = {}
        for type_carte in TypeCarte:
            count = self.count_cards_by_type(type_carte)
            value_sum = self.sum_values_by_type(type_carte)
            summary[type_carte.value] = (count, value_sum)
        
        # Ajouter le total
        summary["TOTAL"] = (self.get_total_count(), self.get_total_value())
        
        return summary
    
    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle du deck.
        
        Returns:
            str: Représentation du deck
        """
        summary = self.get_summary()
        result = ["Deck:"]
        
        for type_name, (count, value_sum) in summary.items():
            result.append(f"  {type_name}: {count} cartes, valeur totale: {value_sum}")
        
        return "\n".join(result)