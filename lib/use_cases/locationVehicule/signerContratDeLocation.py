from datetime import date, timedelta
from typing import Optional

# Importations
from lib.entities.contratLocation import ContratLocation

from lib.repositories.clientRepository import ClientRepository
from lib.repositories.vehiculeRepository import VehiculeRepository
from lib.repositories.assuranceRepository import AssuranceRepository
from lib.repositories.contratRepository import ContratRepository

# Exceptions personnalisées
class ContratLocationError(Exception):
    """Classe de base pour les erreurs liées aux contrats de location"""
    pass


class ClientInexistantError(ContratLocationError):
    """Erreur levée quand le client n'existe pas"""
    pass


class VehiculeInexistantError(ContratLocationError):
    """Erreur levée quand le véhicule n'existe pas"""
    pass


class AssuranceInexistanteError(ContratLocationError):
    """Erreur levée quand l'assurance n'existe pas"""
    pass


class VehiculeNonDisponibleError(ContratLocationError):
    """Erreur levée quand le véhicule n'est pas disponible"""
    pass


class DateInvalideError(ContratLocationError):
    """Erreur levée quand la date est invalide"""
    pass


class EnregistrementContratError(ContratLocationError):
    """Erreur levée lors de l'échec d'enregistrement du contrat"""
    pass


class SignerContratDeLocation:
    @staticmethod
    def main(client_id: int, vehicule_id: int, date_debut: date, duree: int, 
             assurance_id: Optional[int] = None) -> ContratLocation:
        """
        Méthode principale qui exécute le processus de signature d'un contrat de location.
        
        Args:
            client_id: Identifiant du client
            vehicule_id: Identifiant du véhicule
            date_debut: Date de début de la location
            duree: Durée de location en jours
            assurance_id: Identifiant de l'assurance (optionnel)
            
        Returns:
            Le contrat de location créé
            
        Raises:
            ClientInexistantError: Si le client n'existe pas
            VehiculeInexistantError: Si le véhicule n'existe pas
            AssuranceInexistanteError: Si l'assurance spécifiée n'existe pas
            VehiculeNonDisponibleError: Si le véhicule n'est pas disponible pour la période demandée
            DateInvalideError: Si la date de début est dans le passé ou la durée est invalide
            EnregistrementContratError: Si l'enregistrement du contrat échoue
            ContratLocationError: Pour les autres erreurs liées au contrat
        """
        print("=== Système de signature de contrats de location ===")
        
        # Vérifier que la date de début est dans le futur
        if date_debut < date.today():
            raise DateInvalideError("La date de début doit être dans le futur")
        
        # Vérifier que la durée est positive
        if duree <= 0:
            raise DateInvalideError("La durée de location doit être positive")
            
        # Initialiser les repositories (accès aux données)
        client_repo = ClientRepository()
        vehicule_repo = VehiculeRepository()
        assurance_repo = AssuranceRepository()
        contrat_repo = ContratRepository()
        
        try:
            # Récupérer le client par son ID
            client = client_repo.get_by_id(client_id)
            if not client:
                raise ClientInexistantError(f"Le client avec l'ID {client_id} n'existe pas")
                
            # Récupérer le véhicule par son ID
            vehicule = vehicule_repo.get_by_id(vehicule_id)
            if not vehicule:
                raise VehiculeInexistantError(f"Le véhicule avec l'ID {vehicule_id} n'existe pas")
            
            # Récupérer l'assurance si un ID est fourni
            assurance = None
            if assurance_id:
                assurance = assurance_repo.get_by_id(assurance_id)
                if not assurance:
                    raise AssuranceInexistanteError(f"L'assurance avec l'ID {assurance_id} n'existe pas")
            
            # Calculer la date de fin
            date_fin = date_debut + timedelta(days=duree)
            
            # Vérifier si le véhicule est disponible pour la période demandée
            if not vehicule_repo.is_available_between(vehicule_id, date_debut, date_fin):
                marque_modele = f"{vehicule.getMarque()} {vehicule.getModele()}"
                raise VehiculeNonDisponibleError(f"Le véhicule {marque_modele} n'est pas disponible pour la période demandée")
                
            # Calculer le coût de location
            cout = vehicule_repo.calculate_rental_cost(vehicule_id, duree)
            if assurance:
                cout += assurance.getTarif() * duree  # Ajouter le coût de l'assurance
            
            # Création du contrat
            contrat = ContratLocation(
                dateDebut=date_debut,
                duree=duree,
                caution=500.0,  # valeur par défaut
                cout=cout,
                client=client,
                vehicule=vehicule,
                assurance=assurance
            )
            
            # Enregistrer le contrat dans la base de données
            try:
                contrat_id = contrat_repo.save(contrat)
                contrat.id = contrat_id
            except Exception as e:
                raise EnregistrementContratError(f"Erreur lors de l'enregistrement du contrat: {str(e)}")
            
            # Mettre à jour la disponibilité du véhicule
            vehicule_repo.set_availability(vehicule_id, False)
            
            # Afficher les détails du contrat
            print("\nContrat créé avec succès:")
            print(contrat)
            
            # Simulation de la signature
            print("\nSignature du contrat en cours...")
            print("Contrat signé et enregistré!")
            
            # Retour d'informations
            date_fin = date(date_debut.year, date_debut.month, date_debut.day) + timedelta(days=duree)
            print(f"\nRécapitulatif:")
            print(f"  Le véhicule {vehicule.getMarque()} {vehicule.getModele()} est loué à {client.getNom()} {client.getPrenom()}")
            print(f"  Période: du {date_debut} au {date_fin}")
            print(f"  Montant total: {contrat.getCout()} €")
            
            return contrat
            
        except (ClientInexistantError, VehiculeInexistantError, 
                AssuranceInexistanteError, VehiculeNonDisponibleError, 
                DateInvalideError, EnregistrementContratError) as e:
            # Ces exceptions sont déjà des sous-classes de ContratLocationError
            # et contiennent des messages spécifiques, donc on les propage simplement
            print(f"Erreur: {str(e)}")
            raise
            
        except Exception as e:
            # Capturer toute autre exception et la convertir en ContratLocationError
            error_msg = f"Erreur inattendue lors de la création du contrat: {str(e)}"
            print(error_msg)
            raise ContratLocationError(error_msg) from e
            
        finally:
            print("\n=== Fin du programme ===")


# Exemple d'utilisation du script directement (optionnel)
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python signer_contrat.py <client_id> <vehicule_id> [assurance_id] [duree]")
        sys.exit(1)
    
    client_id = int(sys.argv[1])
    vehicule_id = int(sys.argv[2])
    assurance_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
    duree = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    
    try:
        contrat = SignerContratDeLocation.main(client_id, vehicule_id, date.today() + timedelta(days=1), duree, assurance_id)
        print(f"\nSuccès: Contrat créé avec l'ID {contrat.id}")
        sys.exit(0)
    except ContratLocationError as e:
        print(f"\nErreur dans le processus de location: {str(e)}")
        sys.exit(1)