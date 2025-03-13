from typing import Optional, List
import abc
from ..domain.client import Client

class ClientRepositoryPort(abc.ABC):
    # def __init__(self):
    #     if type(self) == ClientRepositoryPort:
    #         raise Exception("Abstract classes can't be instantiated")

    @abc.abstractmethod
    def get_by_id(self, client_id: int) -> Optional[Client]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Client]:
        pass

    @abc.abstractmethod
    def save(self, client: Client) -> int:
        pass

    @abc.abstractmethod
    def delete(self, client_id: int) -> bool:
        pass

    @abc.abstractmethod
    def find_by_name(self, nom: str, prenom: Optional[str] = None) -> List[Client]:
        pass

    @abc.abstractmethod
    def find_by_permis(self, permis: str) -> Optional[Client]:
        pass

    @abc.abstractmethod
    def find_by_email(self, email: str) -> Optional[Client]:
        pass

    @abc.abstractmethod
    def find_with_active_rentals(self) -> List[Client]:
        pass

    @abc.abstractmethod
    def create_client(self, nom: str, prenom: str, permis: str, telephone: str, email: str, voitureLouer=None) -> Client:
        pass
