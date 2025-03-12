class Vehicule:

    def __init__(self, marque: str, modele: str, annee: int, immatriculation: str, kilometrage: int, prix_journalier: float, etat : str, typeVehicule: str):
        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.immatriculation = immatriculation
        self.kilometrage = kilometrage
        self.prix_journalier = prix_journalier
        self.disponible = True 
        self.etat = etat
        self.typeVehicule = typeVehicule

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


# Exemple d'utilisation
# voiture1 = Vehicule("Peugeot", "208", 2021, "AB-123-CD", 25000, 45.0, "Voiture")
# voiture1.afficher_info()
# voiture1.louer()
# voiture1.afficher_info()
# voiture1.retourner(300)
# voiture1.afficher_info()
