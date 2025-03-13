from typing import Optional, List, Dict, Any
from datetime import date
from ..domain.vehicule import Vehicule

class VehiculeRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VehiculeRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialise les données du repository lors de la première création"""
        # Simulation d'une base de données avec une liste de véhicules
        self._vehicules = {}
        self._next_id = 1

    def get_by_id(self, vehicule_id: int) -> Optional[Vehicule]:
        """
        Récupère un véhicule par son ID
        
        Args:
            vehicule_id: L'ID du véhicule à récupérer
            
        Returns:
            Le véhicule correspondant, ou None s'il n'existe pas
        """
        return self._vehicules.get(vehicule_id)

    def get_all(self) -> List[Vehicule]:
        """
        Récupère tous les véhicules
        
        Returns:
            Une liste de tous les véhicules
        """
        return list(self._vehicules.values())

    def get_available(self) -> List[Vehicule]:
        """
        Récupère tous les véhicules disponibles
        
        Returns:
            Une liste des véhicules disponibles
        """
        return [v for v in self._vehicules.values() if v.disponible]
    
    def save(self, vehicule: Vehicule) -> int:
        """
        Sauvegarde un véhicule (création ou mise à jour)
        
        Args:
            vehicule: Le véhicule à sauvegarder
            
        Returns:
            L'ID du véhicule
        """
        if vehicule.id is None:
            vehicule.id = self._next_id
            self._next_id += 1
        self._vehicules[vehicule.id] = vehicule
        return vehicule.id
    
        # Vérifier si le véhicule a déjà un ID
        # if not hasattr(vehicule, 'id') or vehicule.id is None:
        #     vehicule.id = self._next_id
        #     self._next_id += 1
        
        # Sauvegarder ou mettre à jour le véhicule
        # self._vehicules[vehicule.id] = vehicule
        # return vehicule.id

    def delete(self, vehicule_id: int) -> bool:
        """
        Supprime un véhicule par son ID
        
        Args:
            vehicule_id: L'ID du véhicule à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if vehicule_id in self._vehicules:
            del self._vehicules[vehicule_id]
            return True
        return False

    def is_available(self, vehicule_id: int) -> bool:
        """
        Vérifie si un véhicule est disponible
        
        Args:
            vehicule_id: L'ID du véhicule à vérifier
            
        Returns:
            True si le véhicule est disponible, False sinon
        """
        vehicule = self.get_by_id(vehicule_id)
        if vehicule:
            return vehicule.disponible
        return False

    def set_availability(self, vehicule_id: int, disponible: bool) -> bool:
        """
        Définit la disponibilité d'un véhicule
        
        Args:
            vehicule_id: L'ID du véhicule
            disponible: True pour disponible, False pour indisponible
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        vehicule = self.get_by_id(vehicule_id)
        if vehicule:
            if disponible:
                # Logique pour rendre disponible, similaire à retourner() mais sans km
                vehicule.disponible = True
            else:
                # Logique pour rendre indisponible, similaire à louer()
                if vehicule.disponible:
                    vehicule.disponible = False
                    return True
                return False
            return True
        return False
    
    def is_available_between(self, vehicule_id: int, date_debut: date, date_fin: date) -> bool:
        """
        Cette méthode peut être implémentée si vous avez un système de réservation
        qui permet de vérifier la disponibilité entre deux dates spécifiques
        """
        vehicule = self.get_by_id(vehicule_id)
        if not vehicule or not vehicule.disponible:
            return False
        
        # Dans l'implémentation actuelle, un véhicule est soit disponible soit non
        # Pour une vérification plus précise, il faudrait stocker les périodes de réservation
        return vehicule.disponible

    def louer_vehicule(self, vehicule_id: int) -> bool:
        """
        Marque un véhicule comme loué
        
        Args:
            vehicule_id: L'ID du véhicule à louer
            
        Returns:
            True si la location a réussi, False sinon
        """
        vehicule = self.get_by_id(vehicule_id)
        if vehicule:
            return vehicule.louer()
        return False

    def retourner_vehicule(self, vehicule_id: int, km_parcourus: int) -> bool:
        """
        Retourne un véhicule et met à jour son kilométrage
        
        Args:
            vehicule_id: L'ID du véhicule à retourner
            km_parcourus: Kilomètres parcourus pendant la location
            
        Returns:
            True si le retour a réussi, False sinon
        """
        vehicule = self.get_by_id(vehicule_id)
        if vehicule:
            vehicule.retourner(km_parcourus)
            return True
        return False

    def calculate_rental_cost(self, vehicule_id: int, duree: int) -> float:
        """
        Calcule le coût de location d'un véhicule pour une durée donnée
        
        Args:
            vehicule_id: L'ID du véhicule
            duree: Durée de location en jours
            
        Returns:
            Le coût total de la location
        """
        vehicule = self.get_by_id(vehicule_id)
        if not vehicule:
            return 0.0
        
        # Calcul du coût de base (prix journalier * durée)
        return vehicule.prix_journalier * duree

    def find_by_criteria(self, marque: Optional[str] = None, 
                         modele: Optional[str] = None, 
                         disponible: Optional[bool] = None,
                         type_vehicule: Optional[str] = None,
                         prix_max: Optional[float] = None) -> List[Vehicule]:
        """
        Recherche des véhicules selon différents critères
        
        Args:
            marque: Marque du véhicule (optionnel)
            modele: Modèle du véhicule (optionnel)
            disponible: Disponibilité du véhicule (optionnel)
            type_vehicule: Type de véhicule (optionnel)
            prix_max: Prix journalier maximum (optionnel)
            
        Returns:
            Une liste des véhicules correspondant aux critères
        """
        results = []
        for vehicule in self._vehicules.values():
            # Vérifier chaque critère non-None
            if marque and vehicule.marque.lower() != marque.lower():
                continue
            if modele and vehicule.modele.lower() != modele.lower():
                continue
            if disponible is not None and vehicule.disponible != disponible:
                continue
            if type_vehicule and vehicule.typeVehicule != type_vehicule:
                continue
            if prix_max is not None and vehicule.prix_journalier > prix_max:
                continue
            
            results.append(vehicule)
        
        return results
        
    def create_vehicule(self, marque: str, modele: str, annee: int, 
                        immatriculation: str, kilometrage: int, 
                        prix_journalier: float, etat: str, 
                        type_vehicule: str) -> Vehicule:
        """
        Crée un nouveau véhicule et l'ajoute au repository
        
        Args:
            marque: Marque du véhicule
            modele: Modèle du véhicule
            annee: Année de fabrication
            immatriculation: Numéro d'immatriculation
            kilometrage: Kilométrage actuel
            prix_journalier: Prix journalier de location
            etat: État du véhicule
            type_vehicule: Type de véhicule
            
        Returns:
            Le véhicule créé
        """
        vehicule = Vehicule(marque, modele, annee, immatriculation, 
                           kilometrage, prix_journalier, etat, type_vehicule)
        self.save(vehicule)
        return vehicule
