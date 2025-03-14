from datetime import date
from typing import List, Optional
from ..application.VehiculeRepositoryPort import VehiculeRepositoryPort
from ..domain.vehicule import Vehicule
from ..domain.immatriculation import Immatriculation
from ..domain.exceptions import VehiculeNotFoundException, VehiculeNotAvailableException

class InMemoryVehiculeRepository(VehiculeRepositoryPort):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryVehiculeRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._vehicules = {}

    def get_by_immatriculation(self, immatriculation: Immatriculation) -> Optional[Vehicule]:
        vehicule = self._vehicules.get(immatriculation)
        return vehicule

    def get_all(self) -> List[Vehicule]:
        return list(self._vehicules.values())

    def get_available(self) -> List[Vehicule]:
        return [v for v in self._vehicules.values() if v.disponible]

    def save(self, vehicule: Vehicule) -> int:
        self._vehicules[vehicule.immatriculation] = vehicule
        return vehicule.immatriculation

    def delete(self, vehicule: Immatriculation) -> bool:
        if vehicule in self._vehicules:
            del self._vehicules[vehicule]
            return True
        raise VehiculeNotFoundException(f"Véhicule avec l'ID {vehicule} non trouvé pour suppression.")

    def is_available(self, vehicule: Immatriculation) -> bool:
        vehicule = self.get_by_immatriculastion(vehicule)
        return vehicule.disponible

    def set_availability(self, vehicule: Immatriculation, disponible: bool) -> bool:
        vehicule = self.get_by_immatriculation(vehicule)
        vehicule.disponible = disponible
        return True

    def is_available_between(self, vehicule: Immatriculation, date_debut: date, date_fin: date) -> bool:
        vehicule = self.get_by_immatriculation(vehicule)
        if not vehicule.disponible:
            return False
        return vehicule.disponible

    def louer_vehicule(self, vehicule: Immatriculation) -> bool:
        vehicule = self.get_by_immatriculation(vehicule)
        if not vehicule.disponible:
            raise VehiculeNotAvailableException(f"Véhicule avec l'ID {vehicule} n'est pas disponible pour la location.")
        vehicule.louer()
        return True

    def retourner_vehicule(self, vehicule: Immatriculation, km_parcourus: Immatriculation) -> bool:
        vehicule = self.get_by_immatriculation(vehicule)
        vehicule.retourner(km_parcourus)
        return True

    def calculate_rental_cost(self, vehicule: Immatriculation, duree: int) -> float:
        vehicule = self.get_by_immatriculation(vehicule)
        return vehicule.prix_journalier * duree

    def find_by_criteria(self, marque: Optional[str] = None,
                         modele: Optional[str] = None,
                         disponible: Optional[bool] = None,
                         type_vehicule: Optional[str] = None,
                         prix_max: Optional[float] = None) -> List[Vehicule]:
        results = []
        for vehicule in self._vehicules.values():
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
                        immatriculation: Immatriculation, kilometrage: int,
                        prix_journalier: float, etat: str,
                        type_vehicule: str) -> Vehicule:
        vehicule = Vehicule(marque, modele, annee, immatriculation,
                           kilometrage, prix_journalier, etat, type_vehicule)
        self.save(vehicule)
        return vehicule
