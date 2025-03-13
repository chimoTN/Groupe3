# lib/use_cases/locationVehicule/signerContratDeLocation.py
from datetime import date, timedelta
from typing import Optional, Tuple, Dict, Any

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
    Classe implémentant le cas d'utilisation de signature d'un contrat de location
    selon le Design Pattern Sandwich (Three-Layer Architecture).
    """
    
    @staticmethod
    def main(client_id: int, vehicule_id: int, date_debut: date, duree: int, 
             assurance_id: Optional[int] = None) -> ContratLocation:
        """
        Point d'entrée de l'application - Couche de présentation (UI/API)
        
        Args:
            client_id: Identifiant du client
            vehicule_id: Identifiant du véhicule
            date_debut: Date de début de la location
            duree: Durée de location en jours
            assurance_id: Identifiant de l'assurance (optionnel)
            
        Returns:
            Le contrat de location créé
            
        Raises:
            Diverses exceptions définies dans le module contrat_location_exceptions.py
        """
        print("=== Système de signature de contrats de location ===")
        
        try:
            # 1. VALIDATION D'ENTRÉE - Couche de présentation
            SignerContratDeLocation._valider_parametres_entree(date_debut, duree)
            
            # 2. INITIALISATION - Couche de données
            repositories = SignerContratDeLocation._initialiser_repositories()
            
            # 3. LOGIQUE MÉTIER - Couche du milieu
            contrat = SignerContratDeLocation._executer_logique_contrat(
                repositories, client_id, vehicule_id, assurance_id, date_debut, duree
            )
            
            # 4. PRÉSENTATION DES RÉSULTATS - Couche de présentation
            SignerContratDeLocation._presenter_resultats(contrat, date_debut, duree)
            
            return contrat
            
        except (ClientInexistantError, VehiculeInexistantError, 
                AssuranceInexistanteError, VehiculeNonDisponibleError, 
                DateInvalideError, EnregistrementContratError) as e:
            # Ces exceptions sont déjà des sous-classes de ContratLocationError
            print(f"Erreur: {str(e)}")
            raise
            
        except Exception as e:
            # Capturer toute autre exception et la convertir en ContratLocationError
            error_msg = f"Erreur inattendue lors de la création du contrat: {str(e)}"
            print(error_msg)
            raise ContratLocationError(error_msg) from e
            
        finally:
            print("\n=== Fin du programme ===")

    # ===== COUCHE DE PRÉSENTATION =====
    
    @staticmethod
    def _valider_parametres_entree(date_debut: date, duree: int) -> None:
        """
        Valide les paramètres d'entrée - Partie de la couche de présentation.
        
        Args:
            date_debut: Date de début de la location
            duree: Durée de location en jours
            
        Raises:
            DateInvalideError: Si les paramètres ne sont pas valides
        """
        # Vérifier que la date de début est dans le futur
        if date_debut < date.today():
            raise DateInvalideError("La date de début doit être dans le futur")
        
        # Vérifier que la durée est positive
        if duree <= 0:
            raise DateInvalideError("La durée de location doit être positive")
    
    @staticmethod
    def _presenter_resultats(contrat: ContratLocation, date_debut: date, duree: int) -> None:
        """
        Affiche les résultats du contrat - Couche de présentation.
        
        Args:
            contrat: Le contrat de location créé
            date_debut: Date de début de la location
            duree: Durée de location en jours
        """
        # Afficher les détails du contrat
        print("\nContrat créé avec succès:")
        print(contrat)
        
        # Simulation de la signature
        print("\nSignature du contrat en cours...")
        print("Contrat signé et enregistré!")
        
        # Retour d'informations
        date_fin = date(date_debut.year, date_debut.month, date_debut.day) + timedelta(days=duree)
        vehicule = contrat.getVehicule()
        client = contrat.getClient()
        
        print(f"\nRécapitulatif:")
        print(f"  Le véhicule {vehicule.getMarque()} {vehicule.getModele()} est loué à {client.getNom()} {client.getPrenom()}")
        print(f"  Période: du {date_debut} au {date_fin}")
        print(f"  Montant total: {contrat.getCout()} €")

    # ===== COUCHE DE DONNÉES =====
    
    @staticmethod
    def _initialiser_repositories() -> Dict[str, Any]:
        """
        Initialise les repositories - Couche de données.
        
        Returns:
            Un dictionnaire contenant les repositories
        """
        return {
            'client': ClientRepository(),
            'vehicule': VehiculeRepository(),
            'assurance': AssuranceRepository(),
            'contrat': ContratRepository()
        }

    # ===== COUCHE LOGIQUE (MILIEU) =====
    
    @staticmethod
    def _executer_logique_contrat(repositories: Dict[str, Any], 
                                client_id: int, vehicule_id: int, 
                                assurance_id: Optional[int], 
                                date_debut: date, duree: int) -> ContratLocation:
        """
        Exécute la logique métier principale - Couche du milieu.
        
        Args:
            repositories: Dictionnaire contenant les repositories
            client_id: Identifiant du client
            vehicule_id: Identifiant du véhicule
            assurance_id: Identifiant de l'assurance (optionnel)
            date_debut: Date de début de la location
            duree: Durée de location en jours
            
        Returns:
            Le contrat de location créé
            
        Raises:
            Diverses exceptions définies dans le module contrat_location_exceptions.py
        """
        # 1. Récupération des données
        client, vehicule, assurance = SignerContratDeLocation._recuperer_donnees(
            repositories, client_id, vehicule_id, assurance_id
        )
        
        # 2. Vérifier la disponibilité
        date_fin = date_debut + timedelta(days=duree)
        SignerContratDeLocation._verifier_disponibilite(
            repositories['vehicule'], vehicule_id, vehicule, date_debut, date_fin
        )
        
        # 3. Calculer le coût
        cout = SignerContratDeLocation._calculer_cout(
            repositories['vehicule'], vehicule_id, duree, assurance
        )
        
        # 4. Créer et sauvegarder le contrat
        contrat = SignerContratDeLocation._creer_et_sauvegarder_contrat(
            repositories, date_debut, duree, cout, client, vehicule, assurance, vehicule_id
        )
        
        return contrat
    
    @staticmethod
    def _recuperer_donnees(repositories: Dict[str, Any], client_id: int, vehicule_id: int, 
                         assurance_id: Optional[int]) -> Tuple[Any, Any, Optional[Any]]:
        """
        Récupère les données nécessaires depuis les repositories.
        
        Returns:
            Tuple contenant client, vehicule, assurance (qui peut être None)
        
        Raises:
            ClientInexistantError, VehiculeInexistantError, AssuranceInexistanteError
        """
        # Récupérer le client
        client = repositories['client'].get_by_id(client_id)
        if not client:
            raise ClientInexistantError(f"Le client avec l'ID {client_id} n'existe pas")
            
        # Récupérer le véhicule
        vehicule = repositories['vehicule'].get_by_id(vehicule_id)
        if not vehicule:
            raise VehiculeInexistantError(f"Le véhicule avec l'ID {vehicule_id} n'existe pas")
        
        # Récupérer l'assurance si un ID est fourni
        assurance = None
        if assurance_id:
            assurance = repositories['assurance'].get_by_id(assurance_id)
            if not assurance:
                raise AssuranceInexistanteError(f"L'assurance avec l'ID {assurance_id} n'existe pas")
        
        return client, vehicule, assurance
    
    @staticmethod
    def _verifier_disponibilite(vehicule_repo: VehiculeRepository, vehicule_id: int, 
                              vehicule: Any, date_debut: date, date_fin: date) -> None:
        """
        Vérifie si le véhicule est disponible pour la période demandée.
        
        Raises:
            VehiculeNonDisponibleError si le véhicule n'est pas disponible
        """
        if not vehicule_repo.is_available_between(vehicule_id, date_debut, date_fin):
            marque_modele = f"{vehicule.getMarque()} {vehicule.getModele()}"
            raise VehiculeNonDisponibleError(f"Le véhicule {marque_modele} n'est pas disponible pour la période demandée")
    
    @staticmethod
    def _calculer_cout(vehicule_repo: VehiculeRepository, vehicule_id: int, 
                      duree: int, assurance: Optional[Any]) -> float:
        """
        Calcule le coût total de la location, incluant l'assurance si présente.
        
        Returns:
            Le coût total de la location
        """
        # Calculer le coût de base du véhicule
        cout = vehicule_repo.calculate_rental_cost(vehicule_id, duree)
        
        # Ajouter le coût de l'assurance si applicable
        if assurance:
            cout += assurance.getTarif() * duree
            
        return cout
    
    @staticmethod
    def _creer_et_sauvegarder_contrat(repositories: Dict[str, Any], date_debut: date, 
                                    duree: int, cout: float, client: Any, vehicule: Any, 
                                    assurance: Optional[Any], vehicule_id: int) -> ContratLocation:
        """
        Crée le contrat et le sauvegarde dans la base de données.
        
        Returns:
            Le contrat créé et sauvegardé
            
        Raises:
            EnregistrementContratError si l'enregistrement échoue
        """
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
            contrat_id = repositories['contrat'].save(contrat)
            contrat.id = contrat_id
        except Exception as e:
            raise EnregistrementContratError(f"Erreur lors de l'enregistrement du contrat: {str(e)}")
        
        # Mettre à jour la disponibilité du véhicule
        repositories['vehicule'].set_availability(vehicule_id, False)
        
        return contrat


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