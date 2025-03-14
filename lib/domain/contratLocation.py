from datetime import date
from typing import Union, Any, Optional
from typing import List, Optional, Set, Dict, Any, Union
import dataclasses

from .client import Client
from .vehicule import Vehicule
from .assurance import Assurance

@dataclasses.dataclass
class ContratLocation:
    dateDebut: date
    duree: int
    caution: float
    cout: float
    etatInitialDuVehicule: float
    client: Client
    vehicule: Vehicule
    assurance: Optional[Assurance]
    
    def getDateDebut(self) -> date:
        return self._dateDebut
    
    def getDuree(self) -> int:
        return self._duree
    
    def getCaution(self) -> float:
        return self._caution
    
    def getCout(self) -> float:
        return self._cout
    
    def getClient(self) -> Client:
        return self._client
    
    def getVehicule(self) -> Vehicule:
        return self._vehicule
    
    def getAssurance(self) -> Optional[Assurance]:
        return self._assurance
    
    def getDefautsInitiaux(self) -> List[str]:
        return self._defauts_initiaux.copy()  
    
    def getDefautsRestitution(self) -> List[str]:
        return self._defauts_restitution.copy() 
    
    def getDateRestitution(self) -> Optional[date]:
        return self._date_restitution
    
    def getKmDepart(self) -> int:
        return self._km_depart
    
    def getKmRetour(self) -> Optional[int]:
        return self._km_retour
    
    def getCautionRetenue(self) -> Decimal:
        return self._caution_retenue
    
    def estCloture(self) -> bool:
        return self._est_cloture
    
    def setId(self, id: int) -> None:
        self._id = id
    
   
    def setDateDebut(self, dateDebut: date) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        self._dateDebut = dateDebut
    
    def setDuree(self, duree: int) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        if duree <= 0:
            raise ValueError("La durée du contrat doit être positive")
        self._duree = duree
    
    def setCaution(self, caution: float) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        if caution < 0:
            raise ValueError("Le montant de la caution ne peut pas être négatif")
        self._caution = caution
    
    def setCout(self, cout: float) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        if cout < 0:
            raise ValueError("Le coût de location ne peut pas être négatif")
        self._cout = cout
    
    def setClient(self, client: Client) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        self._client = client
    
    def setVehicule(self, vehicule: Vehicule) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        self._vehicule = vehicule
        self._km_depart = vehicule.kilometrage
    
    def setAssurance(self, assurance: Optional[Assurance]) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        self._assurance = assurance
    
    def setDefautsInitiaux(self, defauts: List[str]) -> None:
        if self._est_cloture:
            raise ValueError("Impossible de modifier un contrat clôturé")
        self._defauts_initiaux = defauts.copy()
    
  
    def calculerDateFinPrevue(self) -> date:
        """Calcule la date de fin prévue du contrat"""
        return self._dateDebut + timedelta(days=self._duree)
    
    def enregistrerRestitution(self, 
                              date_restitution: date, 
                              km_retour: int,
                              defauts_restitution: List[str]) -> Decimal:
        """
        Enregistre la restitution du véhicule et calcule les pénalités éventuelles
        
        Args:
            date_restitution: Date de restitution du véhicule
            km_retour: Kilométrage du véhicule à la restitution
            defauts_restitution: Défauts constatés à la restitution
            
        Returns:
            Montant de la caution retenue
            
        Raises:
            ValueError: Si le contrat est déjà clôturé ou si les paramètres sont invalides
        """
        if self._est_cloture:
            raise ValueError("Ce contrat est déjà clôturé")
        
        if date_restitution < self._dateDebut:
            raise ValueError("La date de restitution ne peut pas être antérieure à la date de début")
        
        if km_retour < self._km_depart:
            raise ValueError("Le kilométrage de retour ne peut pas être inférieur au kilométrage de départ")
        
       
        self._date_restitution = date_restitution
        self._km_retour = km_retour
        self._defauts_restitution = defauts_restitution.copy()
        
        nouveaux_defauts = [defaut for defaut in defauts_restitution if defaut not in self._defauts_initiaux]
        
        caution_retenue = self._calculerCautionRetenue(nouveaux_defauts)
        self._caution_retenue = caution_retenue
        
        self._est_cloture = True
        
        return caution_retenue
    
    def _calculerCautionRetenue(self, nouveaux_defauts: List[str]) -> Decimal:
        """
        Calcule le montant de la caution à retenir en fonction des nouveaux défauts
        
        Args:
            nouveaux_defauts: Liste des nouveaux défauts constatés
            
        Returns:
            Montant de la caution à retenir
        """
        if not nouveaux_defauts:
            return Decimal('0.00')
        
        taux_penalite = Decimal('0.10')  
        if self._assurance:
            taux_penalite = Decimal('0.05')  
        
        montant = Decimal(str(self._caution)) * taux_penalite * len(nouveaux_defauts)
        
        return min(montant, Decimal(str(self._caution)))
    
    def verifierNouveauxDefauts(self, defauts_restitution: List[str]) -> List[str]:
        """
        Vérifie quels défauts sont nouveaux par rapport à l'état initial
        
        Args:
            defauts_restitution: Liste des défauts constatés à la restitution
            
        Returns:
            Liste des nouveaux défauts
        """
        return [defaut for defaut in defauts_restitution if defaut not in self._defauts_initiaux]
    
    def estEnRetard(self, date_reference: Optional[date] = None) -> bool:
        """
        Vérifie si le contrat est en retard à une date donnée
        
        Args:
            date_reference: Date de référence (aujourd'hui par défaut)
            
        Returns:
            True si le contrat est en retard, False sinon
        """
        if date_reference is None:
            date_reference = date.today()
            
        date_fin_prevue = self.calculerDateFinPrevue()
        return date_reference > date_fin_prevue and not self._est_cloture
    
    def __str__(self) -> str:
        """Représentation textuelle du contrat de location"""
        assurance_info = f"  Assurance: {self._assurance}\n" if self._assurance else "  Pas d'assurance\n"
        
        defauts_init = ", ".join(self._defauts_initiaux) if self._defauts_initiaux else "Aucun"
        etat_cloture = "Clôturé" if self._est_cloture else "En cours"
        
        return f"Contrat de location {self._id}:\n" \
               f"  Date de début: {self._dateDebut}\n" \
               f"  Durée: {self._duree} jours\n" \
               f"  Date de fin prévue: {self.calculerDateFinPrevue()}\n" \
               f"  Caution: {self._caution} €\n" \
               f"  Coût: {self._cout} €\n" \
               f"  État: {etat_cloture}\n" \
               f"  Défauts initiaux: {defauts_init}\n" \
               f"{assurance_info}" \
               f"  Client: {self._client}\n" \
               f"  Véhicule: {self._vehicule}"