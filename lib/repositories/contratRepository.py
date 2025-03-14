from typing import Optional, List, Dict, Any, Union
from datetime import date, datetime, timedelta
from lib.entities.client import Client
from lib.entities.contratLocation import ContratLocation
from lib.entities.vehicule import Vehicule
from lib.entities.assurance import Assurance

class Contrat:
    """
    Classe pour représenter un contrat de location
    """
    def __init__(self, client: Client, vehicule: Vehicule, date_debut: date, 
                 duree: int, assurance: Optional[Assurance] = None, 
                 caution: float = 0.0):
        self.client = client
        self.vehicule = vehicule
        self.date_debut = date_debut
        self.duree = duree
        self.assurance = assurance
        self.caution = caution
        self.cout_total = vehicule.prix_journalier * duree
        self.date_fin = date_debut + timedelta(days=duree)
        self.est_actif = True
        self.id = None 
        
        client.voitureLouer = vehicule

class ContratRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContratRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialise les données du repository lors de la première création"""
        self._contrats = {}
        self._next_id = 1

    def get_by_id(self, contrat_id: int) -> Optional[Contrat]:
        """
        Récupère un contrat par son ID
        
        Args:
            contrat_id: L'ID du contrat à récupérer
            
        Returns:
            Le contrat correspondant, ou None s'il n'existe pas
        """
        return self._contrats.get(contrat_id)

    def get_all(self) -> List[Contrat]:
        """
        Récupère tous les contrats
        
        Returns:
            Une liste de tous les contrats
        """
        return list(self._contrats.values())

    def save(self, contrat: Contrat) -> int:
        """
        Sauvegarde un contrat (création ou mise à jour)
        
        Args:
            contrat: Le contrat à sauvegarder
            
        Returns:
            L'ID du contrat
        """
        if contrat.id is None:
            contrat.id = self._next_id
            self._next_id += 1
        
        self._contrats[contrat.id] = contrat
        
        contrat.vehicule.louer()
        
        return contrat.id

    def delete(self, contrat_id: int) -> bool:
        """
        Supprime un contrat par son ID
        
        Args:
            contrat_id: L'ID du contrat à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        contrat = self.get_by_id(contrat_id)
        if contrat:
            if contrat.est_actif:
                contrat.client.voitureLouer = None
                contrat.est_actif = False
            
            del self._contrats[contrat_id]
            return True
        return False

    def find_by_client(self, client_id: int) -> List[Contrat]:
        """
        Recherche des contrats par client
        
        Args:
            client_id: L'ID du client
            
        Returns:
            Une liste des contrats pour ce client
        """
        return [c for c in self._contrats.values() if hasattr(c.client, 'id') and c.client.id == client_id]

    def find_by_vehicule(self, vehicule_id: int) -> List[Contrat]:
        """
        Recherche des contrats par véhicule
        
        Args:
            vehicule_id: L'ID du véhicule
            
        Returns:
            Une liste des contrats pour ce véhicule
        """
        return [c for c in self._contrats.values() if hasattr(c.vehicule, 'id') and c.vehicule.id == vehicule_id]

    def find_active_contracts(self, date_reference: Optional[date] = None) -> List[Contrat]:
        """
        Recherche des contrats actifs à une date donnée
        
        Args:
            date_reference: Date de référence (aujourd'hui par défaut)
            
        Returns:
            Une liste des contrats actifs à cette date
        """
        if date_reference is None:
            date_reference = date.today()
            
        return [c for c in self._contrats.values() 
                if c.est_actif and c.date_debut <= date_reference <= c.date_fin]
                
    def close_contract(self, contrat_id: int, km_parcourus: int) -> bool:
        """
        Clôture un contrat et retourne le véhicule
        
        Args:
            contrat_id: ID du contrat à clôturer
            km_parcourus: Kilomètres parcourus pendant la location
            
        Returns:
            True si la clôture a réussi, False sinon
        """
        contrat = self.get_by_id(contrat_id)
        if contrat and contrat.est_actif:

            contrat.vehicule.retourner(km_parcourus)
            

            contrat.client.retourner_voiture(contrat.vehicule, km_parcourus)
            contrat.client.voitureLouer = None
            

            contrat.est_actif = False
            return True
        return False
        
    def create_contrat(self, client: Client, vehicule: Vehicule, 
                       date_debut: Union[date, str], duree: int,
                       assurance: Optional[Assurance] = None) -> Optional[Contrat]:
        """
        Crée un nouveau contrat et l'ajoute au repository
        
        Args:
            client: Le client qui loue
            vehicule: Le véhicule loué
            date_debut: Date de début de la location
            duree: Durée de la location en jours
            assurance: Assurance optionnelle
            
        Returns:
            Le contrat créé ou None si le véhicule n'est pas disponible
        """

        if not vehicule.disponible:
            return None
            

        if isinstance(date_debut, str):
            try:
                date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Format de date invalide. Utilisez le format 'YYYY-MM-DD'")
        
        cout_total = vehicule.prix_journalier * duree
        caution = cout_total * 0.10 
        
     
        contrat = Contrat(
            client=client,
            vehicule=vehicule,
            date_debut=date_debut,
            duree=duree,
            assurance=assurance,
            caution=caution
        )
        
        client.louer_voiture(vehicule)
        
        self.save(contrat)
        
        return contrat

    def trouver_contrat_actif(self, client_id: int, vehicule_id: int) -> Optional[ContratLocation]:
        """
        Recherche un contrat actif pour un client et un véhicule donnés
        
        Args:
            client_id: ID du client
            vehicule_id: ID du véhicule
            
        Returns:
            Le contrat actif s'il existe, sinon None
        """
        contrats_client = self.find_by_client(client_id)
        for contrat in contrats_client:
            if (hasattr(contrat.getVehicule(), 'id') and 
                contrat.getVehicule().id == vehicule_id and
                not contrat.estCloture()):
                return contrat
        return None

