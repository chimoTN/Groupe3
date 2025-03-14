import dataclasses
from typing import List, Optional

from .immatriculation import Immatriculation

@dataclasses.dataclass
class Vehicule:
    marque: str
    modele: str
    annee: int
    immatriculation: Immatriculation
    kilometrage: int
    prix_journalier: float 
    etat: str
    typeVehicule: str
    disponible: bool = True


    def __post_init__(self):
        if self.kilometrage < 0:
            raise ValueError("Le kilométrage ne peut pas être négatif")
        if self.prix_journalier < 0:
            raise ValueError("Le prix journalier ne peut pas être négatif")

    def louer(self) -> bool:
        """
        Marque le véhicule comme loué si disponible
        
        Returns:
            True si la location a réussi, False sinon
        """
        if self._disponible:
            self._disponible = False
            print(f"La voiture {self._marque} {self._modele} a été louée.")
            return True
        else:
            print(f"La voiture {self._marque} {self._modele} est déjà louée.")
            return False

    def retourner(self, nouveaux_km: int, nouvel_etat: str, nouveaux_defauts: Optional[List[str]] = None) -> None:
        """
        Retourne le véhicule et met à jour son état
        
        Args:
            nouveaux_km: Kilométrage à ajouter
            nouvel_etat: Nouvel état général du véhicule
            nouveaux_defauts: Liste des défauts constatés à la restitution
            
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        if nouveaux_km < 0:
            raise ValueError("Le kilométrage ajouté ne peut pas être négatif")
            

        self.etat = nouvel_etat
        

        self.kilometrage += nouveaux_km
        

        if nouveaux_defauts:
            self._defauts = nouveaux_defauts.copy()
        

        self._disponible = True
        
        print(f"La voiture {self._marque} {self._modele} a été retournée avec {nouveaux_km} km supplémentaires.")
        print(f"Nouvel état: {self._etat}")
        if nouveaux_defauts:
            print(f"Défauts constatés: {', '.join(nouveaux_defauts)}")

    def ajouterDefaut(self, defaut: str) -> None:
        """
        Ajoute un défaut à la liste des défauts
        
        Args:
            defaut: Défaut à ajouter
        """
        if defaut not in self._defauts:
            self._defauts.append(defaut)

    def supprimerDefaut(self, defaut: str) -> bool:
        """
        Supprime un défaut de la liste des défauts
        
        Args:
            defaut: Défaut à supprimer
            
        Returns:
            True si le défaut a été supprimé, False s'il n'existait pas
        """
        if defaut in self._defauts:
            self._defauts.remove(defaut)
            return True
        return False

    def afficher_info(self) -> None:
        """Affiche les informations du véhicule"""
        statut = "Disponible" if self._disponible else "Loué"
        defauts = ", ".join(self._defauts) if self._defauts else "Aucun"
        
        print(f"Véhicule: {self.marque} {self.modele} ({self.annee})")
        print(f"Immatriculation: {self.immatriculation}")
        print(f"Type: {self.typeVehicule}")
        print(f"Kilométrage: {self.kilometrage} km")
        print(f"Prix journalier: {self.prix_journalier} €/jour")
        print(f"État: {self.etat}")
        print(f"Défauts: {defauts}")
        print(f"Statut: {statut}")
