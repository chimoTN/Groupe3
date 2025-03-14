from datetime import date
import uuid
from typing import List, Optional

from ..domain.immatriculation import Immatriculation
from ..application.DevisRepositoryPort import DevisRepositoryPort
from ..domain.devis import Devis
from ..domain.exceptions import VehiculeNotFoundException, VehiculeNotAvailableException

class InMemoryDevisRepository(DevisRepositoryPort):
    _instance = None
    _devis: dict[uuid.UUID, list[Devis]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryDevisRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._devis = {}
        self._next_id = 1

    def get_by_immatriculation(self, immatriculation: Immatriculation) -> List[Devis]:
        return [devis for devis in self._devis.get(immatriculation, []) if devis.vehicule.immatriculation == immatriculation]
    
    def get_all(self) -> List[Devis]:
        return list(self._devis.values())
    
    def save(self, devis: Devis):
        self._devis[devis.id] = devis

    def delete(self, devis: Devis):
        del self._devis[devis.id]
    
    def clear(self):
        self._devis = {}