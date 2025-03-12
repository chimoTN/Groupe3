from typing import Optional

class RestitutionVehicule:

    def __init__(self, client, vehicule):
        """
        Use Case pour retourner un véhicule.
        :param client: Repository pour gérer les clients.
        :param vehicule: Repository pour gérer les véhicules.
        """
        self.client = client
        self.vehicule = vehicule

    def execute(self, client_id: str, vehicule_id: str, km_parcourus: int) -> str:
        """
        Exécute le retour du véhicule.

        :param client_id: ID du client qui retourne le véhicule.
        :param vehicule_id: ID du véhicule retourné.
        :param km_parcourus: Nombre de kilomètres parcourus durant la location.
        :return: Message confirmant le retour ou expliquant l'erreur.
        """

        # Récupération du client
        client = self.client.get_by_id(client_id)
        if not client:
            return "❌ Client introuvable."

        # Vérification que le client a bien loué cette voiture
        if not client.voitureLouer or client.voitureLouer.immatriculation != vehicule_id:
            return "❌ Ce client n'a pas loué ce véhicule."

        # Récupération du véhicule
        vehicule = self.vehicule.get_by_id(vehicule_id)
        if not vehicule:
            return "❌ Véhicule introuvable."

        # Retour du véhicule : mise à jour du kilométrage et disponibilité
        vehicule.retourner(km_parcourus)

        # Mise à jour du client : suppression de la voiture louée
        client.voitureLouer = None

        # Enregistrement des mises à jour
        self.client.update(client)
        self.vehicule.update(vehicule)

        return f"✅ Le véhicule {vehicule.marque} {vehicule.modele} ({vehicule.immatriculation}) a été retourné avec {km_parcourus} km supplémentaires."
