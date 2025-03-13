from typing import Optional, List
from ..domain.client import Client

class ClientRepositoryPort:
    def __init__(self):
        if type(self) == ClientRepositoryPort:
            raise Exception("Abstract classes can't be instantiated")

    def get_by_id(self, client_id: int) -> Optional[Client]:
        pass

    def get_all(self) -> List[Client]:
        pass

    def save(self, client: Client) -> int:
        pass

    def delete(self, client_id: int) -> bool:
        pass

    def find_by_name(self, nom: str, prenom: Optional[str] = None) -> List[Client]:
        pass

    def find_by_permis(self, permis: str) -> Optional[Client]:
        pass

    def find_by_email(self, email: str) -> Optional[Client]:
        pass

    def find_with_active_rentals(self) -> List[Client]:
        pass

    def create_client(self, nom: str, prenom: str, permis: str, telephone: str, email: str, voitureLouer=None) -> Client:
        pass
