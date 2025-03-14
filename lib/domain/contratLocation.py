from datetime import date, timedelta
from typing import Optional, List
import dataclasses

from .etat_vehicule import EtatVehicule
from .client import Client
from .vehicule import Vehicule
from .assurance import Assurance

@dataclasses.dataclass
class ContratLocation:
    # Attributs obligatoires
    client: Client
    vehicule: Vehicule
    dateDebut: date
    duree: int
    caution: float
    cout: float
    etatInitialDuVehicule: EtatVehicule
    
    # Attributs optionnels avec valeurs par défaut
    defautsInitiaux: List[str] = dataclasses.field(default_factory=list)
    assurance: Optional[Assurance] = None
    est_cloture: bool = False
    date_restitution: Optional[date] = None
    km_retour: Optional[int] = None
    defauts_restitution: List[str] = dataclasses.field(default_factory=list)
    caution_retenue: float = 0.0
    id: Optional[int] = None
    
    def __post_init__(self):
        """Initialisation après la création de l'instance"""
        # Vérification des valeurs initiales
        if self.duree <= 0:
            raise ValueError("La durée du contrat doit être positive")
        if self.caution < 0:
            raise ValueError("Le montant de la caution ne peut pas être négatif")
        if self.cout < 0:
            raise ValueError("Le coût de location ne peut pas être négatif")
        
        # Récupération du kilométrage de départ
        self.km_depart = self.vehicule.kilometrage
        
        # Création d'une copie de la liste pour éviter le partage de référence
        self.defautsInitiaux = self.defautsInitiaux.copy()
    
    def __setattr__(self, name, value):
        """Méthode appelée lors de l'assignation d'un attribut"""
        # Vérification pour les attributs qui nécessitent contrôle
        if name in ['dateDebut', 'duree', 'caution', 'cout', 'client', 'vehicule', 'assurance', 'defautsInitiaux']:
            if hasattr(self, 'est_cloture') and self.est_cloture:
                raise ValueError(f"Impossible de modifier {name} sur un contrat clôturé")
            
            # Vérifications spécifiques selon l'attribut
            if name == 'duree' and value <= 0:
                raise ValueError("La durée du contrat doit être positive")
            elif name == 'caution' and value < 0:
                raise ValueError("Le montant de la caution ne peut pas être négatif")
            elif name == 'cout' and value < 0:
                raise ValueError("Le coût de location ne peut pas être négatif")
            elif name == 'defautsInitiaux' and isinstance(value, list):
                # Créer une copie pour éviter les références partagées
                value = value.copy()
            elif name == 'vehicule':
                # Mettre à jour km_depart si le véhicule change
                object.__setattr__(self, 'km_depart', value.kilometrage)
                
        # Assignation de la valeur
        object.__setattr__(self, name, value)
    
    def calculerDateFinPrevue(self) -> date:
        """Calcule la date de fin prévue du contrat"""
        return self.dateDebut + timedelta(days=self.duree)
    
    def enregistrerRestitution(self, 
                              date_restitution: date, 
                              km_retour: int,
                              defauts_restitution: List[str]) -> float:
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
        if self.est_cloture:
            raise ValueError("Ce contrat est déjà clôturé")
        
        if date_restitution < self.dateDebut:
            raise ValueError("La date de restitution ne peut pas être antérieure à la date de début")
        
        if km_retour < self.km_depart:
            raise ValueError("Le kilométrage de retour ne peut pas être inférieur au kilométrage de départ")
        
        # Bypass la vérification de __setattr__ car le contrat n'est pas encore clôturé
        object.__setattr__(self, 'date_restitution', date_restitution)
        object.__setattr__(self, 'km_retour', km_retour)
        object.__setattr__(self, 'defauts_restitution', defauts_restitution.copy())
        
        nouveaux_defauts = self.verifierNouveauxDefauts(defauts_restitution)
        
        caution_retenue = self._calculerCautionRetenue(nouveaux_defauts)
        object.__setattr__(self, 'caution_retenue', caution_retenue)
        
        # Marquer le contrat comme clôturé en dernier
        object.__setattr__(self, 'est_cloture', True)
        
        return caution_retenue
    
    def _calculerCautionRetenue(self, nouveaux_defauts: List[str]) -> float:
        """
        Calcule le montant de la caution à retenir en fonction des nouveaux défauts
        
        Args:
            nouveaux_defauts: Liste des nouveaux défauts constatés
            
        Returns:
            Montant de la caution à retenir
        """
        if not nouveaux_defauts:
            return 0.0
        
        taux_penalite = 0.1
        if self.assurance:
            taux_penalite = 0.05  
        
        montant = float(str(self.caution)) * taux_penalite * len(nouveaux_defauts)
        
        return min(montant, float(str(self.caution)))
    
    def verifierNouveauxDefauts(self, defauts_restitution: List[str]) -> List[str]:
        """
        Vérifie quels défauts sont nouveaux par rapport à l'état initial
        
        Args:
            defauts_restitution: Liste des défauts constatés à la restitution
            
        Returns:
            Liste des nouveaux défauts
        """
        return [defaut for defaut in defauts_restitution if defaut not in self.defautsInitiaux]
    
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
        return date_reference > date_fin_prevue and not self.est_cloture
    
    def est_actif(self) -> bool:
        """Indique si le contrat est actif (non clôturé)"""
        return not self.est_cloture
    
    def __str__(self) -> str:
        """Représentation textuelle du contrat de location"""
        assurance_info = f"  Assurance: {self.assurance}\n" if self.assurance else "  Pas d'assurance\n"
        
        defauts_init = ", ".join(self.defautsInitiaux) if self.defautsInitiaux else "Aucun"
        etat_cloture = "Clôturé" if self.est_cloture else "En cours"
        
        id_str = f"{self.id}" if self.id is not None else "Non assigné"
        
        return f"Contrat de location {id_str}:\n" \
               f"  Date de début: {self.dateDebut}\n" \
               f"  Durée: {self.duree} jours\n" \
               f"  Date de fin prévue: {self.calculerDateFinPrevue()}\n" \
               f"  Caution: {self.caution} €\n" \
               f"  Coût: {self.cout} €\n" \
               f"  État: {etat_cloture}\n" \
               f"  Défauts initiaux: {defauts_init}\n" \
               f"{assurance_info}" \
               f"  Client: {self.client}\n" \
               f"  Véhicule: {self.vehicule}"

# Alias pour compatibilité
Contrat = ContratLocation
