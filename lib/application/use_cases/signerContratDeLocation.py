from datetime import date, timedelta
from typing import Optional, List, Tuple, Any
from decimal import Decimal

# Importation des exceptions depuis le fichier séparé
from ..exceptions import (
    ContratLocationError, ClientInexistantError, VehiculeInexistantError,
    AssuranceInexistanteError, VehiculeNonDisponibleError, DateInvalideError,
    EnregistrementContratError
)

# Importations des entités et repositories
from ...domain.contratLocation import ContratLocation
from ...application.ClientRepositoryPort import ClientRepository
from ...application.VehiculeRepositoryPort import VehiculeRepository
from ...application.AssuranceRepositoryPort import AssuranceRepository
from ...application.ContratRepositoryPort import ContratRepository

class SignerContratDeLocation:
    """
    Use case pour la signature d'un contrat de location de véhicule
    """
    
    @staticmethod
    def main(client_id: int, vehicule_id: int, date_debut: date, duree: int,
            assurance_id: Optional[int] = None, 
            defauts_initiaux: Optional[List[str]] = None) -> ContratLocation:
        """
        Point d'entrée principal du use case
        
        Args:
            client_id: ID du client
            vehicule_id: ID du véhicule à louer
            date_debut: Date de début de la location
            duree: Durée en jours
            assurance_id: ID de l'assurance (optionnel)
            defauts_initiaux: Liste des défauts constatés à la signature (optionnel)
            
        Returns:
            Le contrat de location créé
            
        Raises:
            Différentes exceptions si les vérifications échouent
        """
        # Validation des paramètres d'entrée
        SignerContratDeLocation._valider_parametres_entree(date_debut, duree)
        
        try:
            # 1. Récupération des données
            client_repo = ClientRepository()
            vehicule_repo = VehiculeRepository()
            assurance_repo = AssuranceRepository()
            contrat_repo = ContratRepository()
            
            # Récupération du client
            client = client_repo.get_by_id(client_id)
            if not client:
                raise ClientInexistantError(f"Le client avec l'ID {client_id} n'existe pas.")
                
            # Récupération du véhicule
            vehicule = vehicule_repo.get_by_id(vehicule_id)
            if not vehicule:
                raise VehiculeInexistantError(f"Le véhicule avec l'ID {vehicule_id} n'existe pas.")
                
            # Récupération de l'assurance si spécifiée
            assurance = None
            if assurance_id is not None:
                assurance = assurance_repo.get_by_id(assurance_id)
                if not assurance:
                    raise AssuranceInexistanteError(f"L'assurance avec l'ID {assurance_id} n'existe pas.")
            
            # 2. Vérification de la disponibilité du véhicule
            date_fin = date_debut + timedelta(days=duree)
            if not vehicule_repo.is_available_between(vehicule_id, date_debut, date_fin):
                raise VehiculeNonDisponibleError(
                    f"Le véhicule {vehicule.getMarque()} {vehicule.getModele()} n'est pas disponible "
                    f"pour la période du {date_debut} au {date_fin}."
                )
            
            # 3. Calcul du coût
            cout_vehicule = vehicule_repo.calculate_rental_cost(vehicule_id, duree)
            cout_total = cout_vehicule
            
            # Ajouter le coût de l'assurance si spécifiée
            if assurance:
                cout_assurance = Decimal(assurance.getTarif()) * duree
                cout_total += cout_assurance
            
            # 4. Création et enregistrement du contrat sans vérifications supplémentaires
            contrat = ContratLocation(
                dateDebut=date_debut,
                duree=duree,
                caution=Decimal('500.00'),  # Montant fixe
                cout=cout_total,
                client=client,
                vehicule=vehicule,
                assurance=assurance,
                defauts_initiaux=defauts_initiaux or []
            )
            
            # Sauvegarde du contrat
            try:
                contrat_id = contrat_repo.save(contrat)
                contrat.id = contrat_id
            except Exception as e:
                raise EnregistrementContratError(f"Erreur lors de l'enregistrement du contrat: {str(e)}")
            
            # Mettre à jour la disponibilité du véhicule
            vehicule_repo.set_availability(vehicule_id, False)
            
            # Affichage d'un message de confirmation
            client_nom = f"{client.getNom()} {client.getPrenom()}"
            vehicule_desc = f"{vehicule.getMarque()} {vehicule.getModele()}"
            print(f"Contrat de location n°{contrat.id} créé avec succès:")
            print(f"- Client: {client_nom}")
            print(f"- Véhicule: {vehicule_desc}")
            print(f"- Période: du {date_debut} au {date_fin} ({duree} jours)")
            print(f"- Coût total: {cout_total}€")
            if assurance:
                print(f"- Assurance: {assurance.getNom()} - {assurance.getTarif()}€/jour")
            else:
                print("- Aucune assurance souscrite")
            
            return contrat
            
        except (ClientInexistantError, VehiculeInexistantError, 
                AssuranceInexistanteError, VehiculeNonDisponibleError, 
                EnregistrementContratError) as e:
            # Propager les exceptions spécifiques
            raise
        except Exception as e:
            # Convertir les exceptions non spécifiques
            print(f"Erreur inattendue: {str(e)}")
            raise
    
    @staticmethod
    def _valider_parametres_entree(date_debut: date, duree: int) -> None:
        """
        Valide les paramètres d'entrée
        
        Args:
            date_debut: Date de début de location
            duree: Durée en jours
            
        Raises:
            DateInvalideError: Si les critères de validation ne sont pas respectés
        """
        # Vérifier que la date n'est pas dans le passé
        if date_debut < date.today():
            raise DateInvalideError("La date de début ne peut pas être dans le passé.")
        
        # Vérifier que la durée est positive
        if duree <= 0:
            raise DateInvalideError("La durée de location doit être positive.")