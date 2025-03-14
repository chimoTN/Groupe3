from datetime import date, timedelta
from typing import Optional, List
from decimal import Decimal

# Importation des exceptions depuis le fichier séparé
from ..exceptions import (
    ContratLocationException, ClientInexistantException, VehiculeInexistantException,
    AssuranceInexistanteException, VehiculeNonDisponibleException, DateInvalideException,
    EnregistrementContratException
)

# Importations des entités et repositories
from ...domain.contratLocation import ContratLocation
from ...application.ClientRepositoryPort import ClientRepositoryPort
from ...application.VehiculeRepositoryPort import VehiculeRepositoryPort
from ...application.AssuranceRepositoryPort import AssuranceRepositoryPort
from ...application.ContratRepositoryPort import ContratRepositoryPort

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
                raise ClientInexistantException(f"Le client avec l'ID {client_id} n'existe pas.")
                
            # Récupération du véhicule
            vehicule = vehicule_repo.get_by_id(vehicule_id)
            if not vehicule:
                raise VehiculeInexistantException(f"Le véhicule avec l'ID {vehicule_id} n'existe pas.")
                
            # Récupération de l'assurance si spécifiée
            assurance = None
            if assurance_id is not None:
                assurance = assurance_repo.get_by_id(assurance_id)
                if not assurance:
                    raise AssuranceInexistanteException(f"L'assurance avec l'ID {assurance_id} n'existe pas.")
            
            # 2. Vérification de la disponibilité du véhicule
            date_fin = date_debut + timedelta(days=duree)
            if not vehicule_repo.is_available_between(vehicule_id, date_debut, date_fin):
                raise VehiculeNonDisponibleException(
                    f"Le véhicule {vehicule.marque} {vehicule.modele} n'est pas disponible "
                    f"pour la période du {date_debut} au {date_fin}."
                )
            
            # 3. Calcul du coût
            cout_vehicule = vehicule_repo.calculate_rental_cost(vehicule_id, duree)
            cout_total = cout_vehicule
            
            # Ajouter le coût de l'assurance si spécifiée
            if assurance:
                cout_assurance = Decimal(assurance.tarif) * duree
                cout_total += cout_assurance
            
            # 4. Création et enregistrement du contrat
            try:
                # Création du contrat en utilisant le constructeur de ContratLocation
                contrat = ContratLocation(
                    client=client,
                    vehicule=vehicule,
                    dateDebut=date_debut,
                    duree=duree,
                    caution=Decimal('500.00'),  # Montant fixe
                    cout=cout_total,
                    etatInitialDuVehicule=vehicule.etat,  # Ajout de l'état du véhicule
                    defautsInitiaux=defauts_initiaux or [],
                    assurance=assurance
                )
                
                # Sauvegarde du contrat
                contrat_id = contrat_repo.save(contrat)
                # Accès direct à l'attribut id, qui sera vérifié par __setattr__
                contrat.id = contrat_id
            except ValueError as e:
                # Capture des erreurs de validation provenant de ContratLocation.__setattr__
                raise ContratLocationException(f"Erreur lors de la création du contrat: {str(e)}")
            except Exception as e:
                raise EnregistrementContratException(f"Erreur lors de l'enregistrement du contrat: {str(e)}")
            
            # Mettre à jour la disponibilité du véhicule
            vehicule_repo.set_availability(vehicule_id, False)
            
            # Affichage d'un message de confirmation
            client_nom = f"{client.nom} {client.prenom}"
            vehicule_desc = f"{vehicule.marque} {vehicule.modele}"
            print(f"Contrat de location n°{contrat.id} créé avec succès:")
            print(f"- Client: {client_nom}")
            print(f"- Véhicule: {vehicule_desc}")
            print(f"- Période: du {date_debut} au {date_fin} ({duree} jours)")
            print(f"- Coût total: {cout_total}€")
            if assurance:
                print(f"- Assurance: {assurance.nom} - {assurance.tarif}€/jour")
            else:
                print("- Aucune assurance souscrite")
            
            return contrat
            
        except (ClientInexistantException, VehiculeInexistantException, 
                AssuranceInexistanteException, VehiculeNonDisponibleException, 
                EnregistrementContratException, ContratLocationException) as e:
            # Propager les exceptions spécifiques
            raise
        except Exception as e:
            # Convertir les exceptions non spécifiques
            print(f"Erreur inattendue: {str(e)}")
            raise ContratLocationException(f"Erreur inattendue lors de la signature du contrat: {str(e)}")
    
    @staticmethod
    def _valider_parametres_entree(date_debut: date, duree: int) -> None:
        """
        Valide les paramètres d'entrée
        
        Args:
            date_debut: Date de début de location
            duree: Durée en jours
            
        Raises:
            DateInvalideException: Si les critères de validation ne sont pas respectés
        """
        # Vérifier que la date n'est pas dans le passé
        if date_debut < date.today():
            raise DateInvalideException("La date de début ne peut pas être dans le passé.")
        
        # Vérifier que la durée est positive
        if duree <= 0:
            raise DateInvalideException("La durée de location doit être positive.")