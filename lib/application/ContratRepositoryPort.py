from typing import Optional, List, Union
from datetime import date
import abc
from ..domain.client import Client
from ..domain.vehicule import Vehicule
from ..domain.assurance import Assurance
from ..domain.contratLocation import ContratLocation

class ContratRepositoryPort(abc.ABC):
    # def __init__(self):
    #     if type(self) == ContratRepositoryPort:
    #         raise Exception("Abstract classes can't be instantiated")

    @abc.abstractmethod
    def get_by_id(self, contrat_id: int) -> Optional[ContratLocation]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[ContratLocation]:
        pass

    @abc.abstractmethod
    def save(self, contrat: ContratLocation) -> int:
        pass

    @abc.abstractmethod
    def delete(self, contrat_id: int) -> bool:
        pass

    @abc.abstractmethod
    def find_by_client(self, client_id: int) -> List[ContratLocation]:
        pass

    @abc.abstractmethod
    def find_by_vehicule(self, vehicule_id: int) -> List[ContratLocation]:
        pass

    @abc.abstractmethod
    def find_active_contracts(self, date_reference: Optional[date] = None) -> List[ContratLocation]:
        pass

    @abc.abstractmethod
    def close_contract(self, contrat_id: int, km_parcourus: int) -> bool:
        pass

    @abc.abstractmethod
    def create_contrat(self, client: Client, vehicule: Vehicule,
                       date_debut: Union[date, str], duree: int,
                       assurance: Optional[Assurance] = None) -> Optional[ContratLocation]:
        pass
