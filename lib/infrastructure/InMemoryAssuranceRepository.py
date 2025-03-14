from ..application.ClientRepositoryPort import ClientRepositoryPort
from ..domain.client import Client
from ..domain.exceptions import ClientNotFoundException, ClientAlreadyExistsException
from typing import List, Optional

class InMemoryClientRepository(ClientRepositoryPort):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryClientRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._clients = {}
        self._next_id = 1

    def get_by_id(self, client_id: int) -> Optional[Client]:
        client = self._clients.get(client_id)
        if client is None:
            raise ClientNotFoundException(f"Client avec l'ID {client_id} non trouvé.")
        return client

    def get_all(self) -> List[Client]:
        return list(self._clients.values())

    def save(self, client: Client) -> int:
        if not hasattr(client, 'id') or client.id is None:
            client.id = self._next_id
            self._next_id += 1
        self._clients[client.id] = client
        return client.id

    def delete(self, client_id: int) -> bool:
        if client_id in self._clients:
            del self._clients[client_id]
            return True
        raise ClientNotFoundException(f"Client avec l'ID {client_id} non trouvé pour suppression.")

    def find_by_name(self, nom: str, prenom: Optional[str] = None) -> List[Client]:
        results = []
        for client in self._clients.values():
            if client.nom.lower() == nom.lower():
                if prenom is None or client.prenom.lower() == prenom.lower():
                    results.append(client)
        if not results:
            raise ClientNotFoundException(f"Client avec le nom '{nom}' et prénom '{prenom}' non trouvé.")
        return results

    def find_by_permis(self, permis: str) -> Optional[Client]:
        for client in self._clients.values():
            if client.permis == permis:
                return client
        raise ClientNotFoundException(f"Client avec le permis '{permis}' non trouvé.")

    def find_by_email(self, email: str) -> Optional[Client]:
        for client in self._clients.values():
            if client.email.lower() == email.lower():
                return client
        raise ClientNotFoundException(f"Client avec l'email '{email}' non trouvé.")

    def find_with_active_rentals(self) -> List[Client]:
        return [client for client in self._clients.values() if client.historique_locations]

    def create_client(self, nom: str, prenom: str, permis: str, telephone: str, email: str, voitureLouer=None) -> Client:
        if any(client.permis == permis for client in self._clients.values()):
            raise ClientAlreadyExistsException(f"Un client avec le permis '{permis}' existe déjà.")

        client = Client(nom, prenom, permis, telephone, email, voitureLouer)
        self.save(client)
        return client
