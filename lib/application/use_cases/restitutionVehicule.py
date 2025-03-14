from typing import Optional, List, Tuple, Dict, Any

from lib.infrastructure.InMemoryClientRepository import InMemoryClientRepository
from lib.infrastructure.InMemoryVehiculeRepository import InMemoryVehiculeRepository
from lib.infrastructure.InMemoryContratRepository import InMemoryContratRepository

from lib.domain.contratLocation import ContratLocation
from lib.domain.client import Client
from lib.domain.vehicule import Vehicule


class RestitutionVehicule:
    """
    Cas d'usage permettant la restitution d'un véhicule par un client,
    avec vérification de l'état par rapport à celui de départ et calcul
    des pénalités éventuelles.
    """

    def __init__(self,
                 client_repository: InMemoryClientRepository,
                 vehicule_repository: InMemoryVehiculeRepository,
                 contrat_repository: InMemoryContratRepository):
        self.client_repository = client_repository
        self.vehicule_repository = vehicule_repository
        self.contrat_repository = contrat_repository

    def restituer_vehicule(self,
                       client_id: int,
                       vehicule_id: int,
                       km_parcourus: int,
                       etat_restitution: str,
                       defauts_restitution: Optional[List[str]] = None) -> Tuple[Optional[Vehicule], float]:
        """
        Permet de gérer la restitution d'un véhicule par un client.

        Args:
            client_id: L'ID du client qui retourne le véhicule
            vehicule_id: L'ID du véhicule retourné
            km_parcourus: Le nombre de kilomètres effectués depuis la location
            etat_restitution: L'état général du véhicule ("Nickel", "Sale", "Endommagé", "Volé")
            defauts_restitution: Liste détaillée des défauts constatés à la restitution

        Returns:
            Tuple contenant:
                - L'objet Vehicule mis à jour, ou None s'il y a une erreur
                - Le montant de la caution retenue (0 si pas de problème)
        """
        try:
            
            etat_restitution = etat_restitution.capitalize()
            defauts_restitution = defauts_restitution or []

            client = self.client_repository.get_by_id(client_id)
            vehicule = self.vehicule_repository.get_by_id(vehicule_id)

            if not client or not vehicule:
                print("Restitution échouée : client ou véhicule introuvable.")
                return None, 0.0

            if vehicule not in client.historique_locations:
                print("Restitution échouée : ce véhicule n'est pas loué par ce client.")
                return None, 0.0

            contrat = self.contrat_repository.trouver_contrat_actif(client_id, vehicule_id)
            if not contrat:
                print("Restitution échouée : aucun contrat actif trouvé pour ce client et ce véhicule.")
                return None, 0.0

            from datetime import date
            montant_caution_retenue = contrat.enregistrerRestitution(
                date_restitution=date.today(),
                km_retour=vehicule.kilometrage + km_parcourus,
                defauts_restitution=defauts_restitution
            )

            vehicule.retourner(km_parcourus, etat_restitution, defauts_restitution)

            client.historique_locations.remove(vehicule)

            self.vehicule_repository.save(vehicule)
            self.client_repository.save(client)
            self.contrat_repository.save(contrat)

            if montant_caution_retenue > 0:
                print(f"Attention: {montant_caution_retenue}€ de caution retenue pour les dégâts constatés.")
            
            print(f"Le véhicule {vehicule.marque} {vehicule.modele} (ID: {vehicule.immatriculation}) "
                f"a été restitué par {client.nom} {client.prenom} avec l'état '{vehicule.etat}'.")
                
            return vehicule, float(montant_caution_retenue)
        
        except Exception as e:
            print(f"Erreur lors de la restitution: {str(e)}")
            raise
