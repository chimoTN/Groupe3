from datetime import date
from typing import Union, Any, Optional

from .client import Client
from .vehicule import Vehicule
from .assurance import Assurance

class ContratLocation:
    def __init__(self, 
                 dateDebut: date, 
                 duree: int, 
                 caution: float, 
                 cout: float,
                 client: Client,
                 vehicule: Vehicule,
                 assurance: Optional[Assurance] = None,
                 etatInitialDuVehicule: float = 100.0) -> None:
        """
        Initialise un contrat de location
        
        Args:
            dateDebut: Date de début du contrat
            duree: Durée du contrat (en jours)
            caution: Montant de la caution en euros
            cout: Coût de la location en euros
            client: Objet Client qui contracte la location
            vehicule: Véhicule concerné par la location
            assurance: Assurance souscrite (optionnelle)
            etatInitialDuVehicule: État initial du véhicule (pourcentage)
        """
        self.dateDebut: date = dateDebut
        self.duree: int = duree
        self.caution: float = caution
        self.cout: float = cout
        self.etatInitialDuVehicule: float = etatInitialDuVehicule
        self.client: Client = client
        self.vehicule: Vehicule = vehicule
        self.assurance: Optional[Assurance] = assurance
    
    def getDateDebut(self) -> date:
        return self.dateDebut
    
    def getDuree(self) -> int:
        return self.duree
    
    def getCaution(self) -> float:
        return self.caution
    
    def getCout(self) -> float:
        return self.cout
    
    def getClient(self) -> Client:
        return self.client
    
    def getVehicule(self) -> Vehicule:
        return self.vehicule
    
    def getAssurance(self) -> Optional[Assurance]:
        return self.assurance
    
    def getEtatInitialDuVehicule(self) -> float:
        return self.etatInitialDuVehicule
    
    def setDateDebut(self, dateDebut: date) -> None:
        self.dateDebut = dateDebut
    
    def setDuree(self, duree: int) -> None:
        self.duree = duree
    
    def setCaution(self, caution: float) -> None:
        self.caution = caution
    
    def setCout(self, cout: float) -> None:
        self.cout = cout
    
    def setClient(self, client: Client) -> None:
        self.client = client
    
    def setVehicule(self, vehicule: Vehicule) -> None:
        self.vehicule = vehicule
    
    def setAssurance(self, assurance: Optional[Assurance]) -> None:
        self.assurance = assurance
    
    def setEtatInitialDuVehicule(self, etatInitialDuVehicule: float) -> None:
        self.etatInitialDuVehicule = etatInitialDuVehicule
        
    def __str__(self) -> str:
        """Représentation textuelle du contrat de location"""
        assurance_info = f"  Assurance: {self.assurance}\n" if self.assurance else "  Pas d'assurance\n"
        
        return f"Contrat de location:\n" \
               f"  Date de début: {self.dateDebut}\n" \
               f"  Durée: {self.duree} jours\n" \
               f"  Caution: {self.caution} €\n" \
               f"  Coût: {self.cout} €\n" \
               f"  État initial: {self.etatInitialDuVehicule}%\n" \
               f"{assurance_info}" \
               f"  Client: {self.client}\n" \
               f"  Véhicule: {self.vehicule}"