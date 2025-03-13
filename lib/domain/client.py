import dataclasses
from .permis import Permis
from .telephone import Telephone
from .email import Email

@dataclasses.dataclass
class Client:
    nom: str
    prenom: str
    permis: Permis
    telephone: Telephone
    email: Email
    voitureLouer: None
    historique_locations: list[str] = dataclasses.field(default_factory=list)

    def louer_voiture(self, voiture) -> bool:
        """Ajoute une voiture à l'historique des locations si elle est disponible."""
        if voiture.louer():
            self.historique_locations.append(voiture)
            print(f"{self.nom} {self.prenom} a loué la voiture {voiture.marque} {voiture.modele}.")
            return True
        return False

    def retourner_voiture(self, voiture, km_parcourus: int) -> None:
        """Retourne la voiture et la supprime de l'historique des locations."""
        if voiture in self.historique_locations:
            voiture.retourner(km_parcourus)
            self.historique_locations.remove(voiture)
            print(f"{self.nom} {self.prenom} a retourné la voiture {voiture.marque} {voiture.modele}.")
        else:
            print(f"{self.nom} {self.prenom} n'a pas cette voiture en location.")


    def afficher_info(self) -> None:
        """Affiche les informations du client et ses locations en cours."""
        print(f"Client: {self.nom} {self.prenom}\n"
              f"Permis: {self.permis}\n"
              f"Téléphone: {self.telephone}\n"
              f"Email: {self.email}\n"
              f"Locations en cours: {len(self.historique_locations)}\n")

    @staticmethod
    def osef() -> None:
        print("osef")
