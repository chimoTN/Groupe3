from ..ClientRepositoryPort import ClientRepositoryPort
from ..VehiculeRepositoryPort import VehiculeRepositoryPort

from typing import Optional
from ...domain.vehicule import Vehicule

class RestitutionVehicule:

    """
    Cas d'usage permettant la restitution d'un véhicule par un client,
    avec mise à jour de l'état selon plusieurs scénarios :
      - nickel
      - sale
      - endommagé
      - volé
    """

    def __init__(self,
                 client_repository: ClientRepositoryPort,
                 vehicule_repository: VehiculeRepositoryPort):
        self.client_repository = client_repository
        self.vehicule_repository = vehicule_repository

    def restituer_vehicule(self,
                           client_id: int,
                           vehicule_id: int,
                           km_parcourus: int,
                           etat_restitution: str) -> Optional[Vehicule]:
        """
        Permet de gérer la restitution d'un véhicule par un client.

        :param client_id: L'ID du client qui retourne le véhicule
        :param vehicule_id: L'ID du véhicule retourné
        :param km_parcourus: Le nombre de kilomètres effectués depuis la location
        :param etat_restitution: Valeur parmi ("nickel", "sale", "endommagé", "volé")
        :return: L'objet Vehicule mis à jour, ou None s'il y a une erreur
        """

        # 1. Récupérer le client et le véhicule via les repositories
        client = self.client_repository.get_by_id(client_id)
        vehicule = self.vehicule_repository.get_by_immatriculation(vehicule_id)

        if not client or not vehicule:
            print("Restitution échouée : client ou véhicule introuvable.")
            return None

        # 2. Vérifier que le client a bien loué ce véhicule
        #    (i.e. qu'il se trouve dans historique_locations)
        if vehicule not in client.historique_locations:
            print("Restitution échouée : ce véhicule n'est pas loué par ce client.")
            return None
            

        # 3. Mettre à jour l'état du véhicule selon l’état constaté au retour
        #    On imagine que l’attribut `etat` du véhicule peut prendre des valeurs
        #    comme "Nickel", "Sale", "Endommagé", "Volé", etc.
        #    À vous d’adapter la logique métier si nécessaire.

        # Normalisation basique de la saisie : on met tout en minuscule
        etat_restitution = etat_restitution.lower()

        if etat_restitution == "nickel":
            vehicule.etat = "Nickel"
        elif etat_restitution == "sale":
            vehicule.etat = "Sale"
        elif etat_restitution == "endommagé":
            vehicule.etat = "Endommagé"
        elif etat_restitution == "volé":
            vehicule.etat = "Volé"
            # Exemple supplémentaire : si c'est volé, on peut imaginer un traitement
            # spécifique (signalement, statut particulier, etc.)
            # vehicule.disponible = False  # Par exemple, un véhicule volé n’est plus dispo
        else:
            print(f"État de restitution non reconnu : {etat_restitution}")
            return None

        # 4. Mettre à jour le kilométrage du véhicule
        vehicule.kilometrage += km_parcourus

        # 5. Rendre le véhicule de nouveau disponible, sauf si volé
        if vehicule.etat != "Volé":
            vehicule.disponible = True

        # 6. Retirer le véhicule de l’historique des locations du client
        client.historique_locations.remove(vehicule)

        # 7. Persister les changements dans les repositories
        self.vehicule_repository.save(vehicule)
        self.client_repository.save(client)

        # 8. Retourner l’objet véhicule mis à jour
        print(f"Le véhicule {vehicule.marque} {vehicule.modele} (ID: {vehicule.immatriculation}) "
              f"a été restitué par {client.nom} {client.prenom} avec l'état '{vehicule.etat}'.")
        return vehicule
