# infrastructure/adapters.py

from ..application.ContratRepositoryPort import ContratRepositoryPort
from ..domain.contratLocation import Contrat
from ..domain.assurance import Assurance
from ..domain.client import Client
from ..domain.vehicule import Vehicule
from ..domain.exceptions import (
    ContratNotFoundException,
    VehiculeNotAvailableException,
    ContratNotActiveException,
    InvalidDateFormatException
)
from typing import Optional, List, Union
from datetime import date, datetime

class InMemoryContratRepository(ContratRepositoryPort):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryContratRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._contrats = {}
        self._next_id = 1

    def get_by_id(self, contrat_id: int) -> Optional[Contrat]:
        contrat = self._contrats.get(contrat_id)
        if contrat is None:
            raise ContratNotFoundException(f"Contrat avec l'ID {contrat_id} non trouvé.")
        return contrat

    def get_all(self) -> List[Contrat]:
        return list(self._contrats.values())

    def save(self, contrat: Contrat) -> int:
        if contrat.id is None:
            contrat.id = self._next_id
            self._next_id += 1
        self._contrats[contrat.id] = contrat
        contrat.vehicule.louer()
        return contrat.id

    def delete(self, contrat_id: int) -> bool:
        contrat = self.get_by_id(contrat_id)
        if contrat:
            if contrat.est_actif:
                contrat.client.voitureLouer = None
                contrat.est_actif = False
            del self._contrats[contrat_id]
            return True
        return False

    def find_by_client(self, client_id: int) -> List[Contrat]:
        return [c for c in self._contrats.values() if hasattr(c.client, 'id') and c.client.id == client_id]

    def find_by_vehicule(self, vehicule_id: int) -> List[Contrat]:
        return [c for c in self._contrats.values() if hasattr(c.vehicule, 'id') and c.vehicule.id == vehicule_id]

    def find_active_contracts(self, date_reference: Optional[date] = None) -> List[Contrat]:
        if date_reference is None:
            date_reference = date.today()
        return [c for c in self._contrats.values() if c.est_actif and c.date_debut <= date_reference <= c.date_fin]

    def close_contract(self, contrat_id: int, km_parcourus: int) -> bool:
        contrat = self.get_by_id(contrat_id)
        if contrat and contrat.est_actif:
            contrat.vehicule.retourner(km_parcourus)
            contrat.client.retourner_voiture(contrat.vehicule, km_parcourus)
            contrat.client.voitureLouer = None
            contrat.est_actif = False
            return True
        raise ContratNotActiveException(f"Contrat avec l'ID {contrat_id} n'est pas actif.")

    def create_contrat(self, client: Client, vehicule: Vehicule,
                       date_debut: Union[date, str], duree: int,
                       assurance: Optional[Assurance] = None) -> Optional[Contrat]:
        if not vehicule.disponible:
            raise VehiculeNotAvailableException(f"Véhicule avec l'ID {vehicule.id} n'est pas disponible.")

        if isinstance(date_debut, str):
            try:
                date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            except ValueError:
                raise InvalidDateFormatException("Format de date invalide. Utilisez le format 'YYYY-MM-DD'")

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
