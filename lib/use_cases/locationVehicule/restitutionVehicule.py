from typing import Optional
from lib.entities.client import Client
from lib.entities.vehicule import Vehicule 

class RestitutionVehicule:
    def __init__(self, client, vehicule):
        self.client = client
        self.vehicule = vehicule

    def execute(self, client_id: str, vehicule_id: str, km_parcourus: int) -> str:
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

        # Retour du véhicule avec l'état par défaut "Bon état"
        vehicule.retourner(km_parcourus, "Bon état")  # Ajout du paramètre manquant

        # Mise à jour du client
        client.voitureLouer = None

        # Enregistrement des mises à jour
        self.client.update(client)
        self.vehicule.update(vehicule)

        return f"✅ Le véhicule {vehicule.marque} {vehicule.modele} ({vehicule.immatriculation}) a été retourné avec {km_parcourus} km supplémentaires."