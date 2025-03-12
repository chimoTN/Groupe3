from datetime import date, datetime, timedelta
from typing import Optional, Union

from lib.entities.client import Client
from lib.entities.vehicule import Vehicule
from lib.entities.assurance import Assurance
from lib.entities.contratLocation import ContratLocation
from lib.repositories.clientRepository import ClientRepository
from lib.repositories.vehiculeRepository import VehiculeRepository
from lib.repositories.assuranceRepository import AssuranceRepository
from lib.repositories.contratRepository import ContratRepository

#TO MOVE ----------------------------------------------------------------------
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

class EnregistrementContratError(ContratLocationError):
    """Erreur levée lors de l'échec d'enregistrement du contrat"""
    pass

class DateInvalideError(ContratLocationError):
    """Erreur levée quand la date de début est invalide"""
    pass

#TO MOVE ----------------------------------------------------------------------

class SignerContratDeLocation:
    @staticmethod
    def main(client_id: int, vehicule_id: int, date_debut: Union[date, str], duree: int, 
             assurance_id: Optional[int] = None) -> ContratLocation:
        """
        Méthode principale qui exécute le processus de signature d'un contrat de location.
        
        Args:
            client_id: Identifiant du client
            vehicule_id: Identifiant du véhicule
            date_debut: Date de début de la location (objet date ou chaîne au format 'YYYY-MM-DD')
            duree: Durée de location en jours
            assurance_id: Identifiant de l'assurance (optionnel)
            
        Returns:
            Le contrat de location créé
            
        Raises:
            ClientInexistantError: Si le client n'existe pas
            VehiculeInexistantError: Si le véhicule n'existe pas
            AssuranceInexistanteError: Si l'assurance spécifiée n'existe pas
            VehiculeNonDisponibleError: Si le véhicule n'est pas disponible
            DateInvalideError: Si la date de début est invalide
            EnregistrementContratError: Si l'enregistrement du contrat échoue
            ContratLocationError: Pour les autres erreurs liées au contrat
        """
        print("=== Système de signature de contrats de location ===")
        
        # Traitement de la date de début
        if isinstance(date_debut, str):
            try:
                date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            except ValueError:
                raise DateInvalideError(f"Format de date invalide. Utilisez le format 'YYYY-MM-DD'")
                
        # Vérifier que la date n'est pas dans le passé
        if date_debut < date.today():
            raise DateInvalideError("La date de début ne peut pas être dans le passé")
        
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
            
            # Vérifier si le véhicule est disponible pour la période demandée
            date_fin = date_debut + timedelta(days=duree)
            if not vehicule_repo.is_available_between(vehicule_id, date_debut, date_fin):
                marque_modele = f"{vehicule.getMarque()} {vehicule.getModele()}"
                raise VehiculeNonDisponibleError(
                    f"Le véhicule {marque_modele} n'est pas disponible entre le {date_debut} et le {date_fin}")
                
            # Récupérer l'assurance si un ID est fourni
            assurance = None
            if assurance_id:
                assurance = assurance_repo.get_by_id(assurance_id)
                if not assurance:
                    raise AssuranceInexistanteError(f"L'assurance avec l'ID {assurance_id} n'existe pas")
            
            # Calculer le coût de location
            cout = vehicule_repo.calculate_rental_cost(vehicule_id, duree)
            if assurance:
                cout += assurance.getTarif() * duree  # Ajouter le coût de l'assurance
                
            # Calculer la caution (10% du prix du contrat)
            caution = cout * 0.1
            
            # Création du contrat
            contrat = ContratLocation(
                dateDebut=date_debut,
                duree=duree,
                caution=caution,
                cout=cout,
                client=client,
                vehicule=vehicule,
                assurance=assurance
            )
            
            # Enregistrer le contrat dans la base de données
            try:
                contrat_id = contrat_repo.save(contrat)
                # Attacher l'ID au contrat
                contrat.id = contrat_id
            except Exception as e:
                raise EnregistrementContratError(f"Erreur lors de l'enregistrement du contrat: {str(e)}")
            
            # Mettre à jour la disponibilité du véhicule
            vehicule_repo.reserve(vehicule_id, date_debut, date_fin)
            
            # Afficher les détails du contrat
            print("\nContrat créé avec succès:")
            print(contrat)
            
            # Simulation de la signature
            print("\nSignature du contrat en cours...")
            print("Contrat signé et enregistré!")
            
            # Retour d'informations
            print(f"\nRécapitulatif:")
            print(f"  Le véhicule {vehicule.getMarque()} {vehicule.getModele()} est loué à {client.getNom()} {client.getPrenom()}")
            print(f"  Période: du {date_debut} au {date_fin}")
            print(f"  Montant total: {contrat.getCout()} €")
            print(f"  Caution: {contrat.getCaution()} €")
            
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


# Exemple d'utilisation du script directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python signer_contrat.py <client_id> <vehicule_id> <date_debut> <duree> [assurance_id]")
        print("  <date_debut>: format YYYY-MM-DD")
        sys.exit(1)
    
    client_id = int(sys.argv[1])
    vehicule_id = int(sys.argv[2])
    date_debut = sys.argv[3]
    duree = int(sys.argv[4])
    assurance_id = int(sys.argv[5]) if len(sys.argv) > 5 else None
    
    try:
        contrat = SignerContratDeLocation.main(client_id, vehicule_id, date_debut, duree, assurance_id)
        print(f"\nSuccès: Contrat créé avec l'ID {contrat.id}")
        print(f"Caution : {contrat.getCaution()} € (10% du prix total)")
        sys.exit(0)
    except ClientInexistantError as e:
        print(f"\nErreur: Client invalide - {str(e)}")
        sys.exit(2)
    except VehiculeInexistantError as e:
        print(f"\nErreur: Véhicule invalide - {str(e)}")
        sys.exit(3)
    except AssuranceInexistanteError as e:
        print(f"\nErreur: Assurance invalide - {str(e)}")
        sys.exit(4)
    except VehiculeNonDisponibleError as e:
        print(f"\nErreur: Véhicule non disponible - {str(e)}")
        sys.exit(5)
    except DateInvalideError as e:
        print(f"\nErreur: Date invalide - {str(e)}")
        sys.exit(6)
    except ContratLocationError as e:
        print(f"\nErreur dans le processus de location: {str(e)}")
        sys.exit(1)