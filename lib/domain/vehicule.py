import dataclasses
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

    def louer(self) -> bool:
        """Marque la voiture comme louée si elle est disponible."""
        if self.disponible:
            self.disponible = False
            print(f"La voiture {self.marque} {self.modele} ({self.immatriculation}) a été louée.")
            return True
        else:
            print(f"La voiture {self.marque} {self.modele} ({self.immatriculation}) est déjà louée.")
            return False

    def retourner(self, nouveaux_km: int, nouvel_etat: str) -> None:
        """Retourne la voiture et met à jour le kilométrage."""
        if not self.disponible:
            self.kilometrage += nouveaux_km
            self.disponible = True
            self.etat = nouvel_etat
            print(f"La voiture {self.marque} {self.modele} ({self.immatriculation}) a été retournée avec {nouveaux_km} km de plus et un état '{self.etat}'.")
        else:
            print(f"La voiture {self.marque} {self.modele} ({self.immatriculation}) a été retournée avec {nouveaux_km} km de plus et un état '{self.etat}'.")

    def afficher_info(self) -> None:
        """Affiche les informations de la voiture."""
        statut = "Disponible" if self.disponible else "Louée"
        print(f"Voiture: {self.marque} {self.modele} ({self.annee})\n"
              f"Immatriculation: {self.immatriculation}\n"
              f"Kilométrage: {self.kilometrage} km\n"
              f"Prix journalier: {self.prix_journalier} €/jour\n"
              f"Statut: {statut}\n")

    def to_dict(self):
        return {
            'marque': self.marque,
            'modele': self.modele,
            'annee': self.annee,
            'immatriculation': str(self.immatriculation),
            'kilometrage': self.kilometrage,
            'prix_journalier': self.prix_journalier,
            'etat': self.etat,
            'typeVehicule': self.typeVehicule,
            'disponible': self.disponible
        }