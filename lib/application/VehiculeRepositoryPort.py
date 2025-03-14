from typing import Optional, List
from datetime import date
import abc
from ..domain.vehicule import Vehicule

class VehiculeRepositoryPort(abc.ABC):
    # def __init__(self):
    #     if type(self) == VehiculeRepositoryPort:
    #         raise Exception("Abstract classes can't be instantiated")
        
    @abc.abstractmethod
    def get_by_immatriculation(self, vehicule_id: int) -> Optional[Vehicule]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Vehicule]:
        pass

    @abc.abstractmethod
    def get_available(self) -> List[Vehicule]:
        pass

    @abc.abstractmethod
    def save(self, vehicule: Vehicule) -> int:
        pass

    @abc.abstractmethod
    def delete(self, vehicule_id: int) -> bool:
        pass

    @abc.abstractmethod
    def is_available(self, vehicule_id: int) -> bool:
        pass

    @abc.abstractmethod
    def set_availability(self, vehicule_id: int, disponible: bool) -> bool:
        pass

    @abc.abstractmethod
    def is_available_between(self, vehicule_id: int, date_debut: date, date_fin: date) -> bool:
        pass

    @abc.abstractmethod
    def louer_vehicule(self, vehicule_id: int) -> bool:
        pass

    @abc.abstractmethod
    def retourner_vehicule(self, vehicule_id: int, km_parcourus: int) -> bool:
        pass

    @abc.abstractmethod
    def calculate_rental_cost(self, vehicule_id: int, duree: int) -> float:
        pass

    @abc.abstractmethod
    def find_by_criteria(self, marque: Optional[str] = None,
                         modele: Optional[str] = None,
                         disponible: Optional[bool] = None,
                         type_vehicule: Optional[str] = None,
                         prix_max: Optional[float] = None) -> List[Vehicule]:
        pass

    @abc.abstractmethod
    def create_vehicule(self, marque: str, modele: str, annee: int,
                        immatriculation: str, kilometrage: int,
                        prix_journalier: float, etat: str,
                        type_vehicule: str) -> Vehicule:
        pass
