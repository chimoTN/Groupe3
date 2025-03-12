from typing import Optional, List, Dict, Any
from lib.entities.client import Client
from lib.entities.vehicule import Vehicule

class ClientRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClientRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialise les données du repository lors de la première création"""
        # Simulation d'une base de données avec une liste de clients
        self._clients = {}
        self._next_id = 1

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Récupère un client par son ID
        
        Args:
            client_id: L'ID du client à récupérer
            
        Returns:
            Le client correspondant, ou None s'il n'existe pas
        """
        return self._clients.get(client_id)

    def get_all(self) -> List[Client]:
        """
        Récupère tous les clients
        
        Returns:
            Une liste de tous les clients
        """
        return list(self._clients.values())

    def save(self, client: Client) -> int:
        """
        Sauvegarde un client (création ou mise à jour)
        
        Args:
            client: Le client à sauvegarder
            
        Returns:
            L'ID du client
        """
        # Vérifier si le client a déjà un ID
        if not hasattr(client, 'id') or client.id is None:
            client.id = self._next_id
            self._next_id += 1
        
        # Sauvegarder ou mettre à jour le client
        self._clients[client.id] = client
        return client.id

    def delete(self, client_id: int) -> bool:
        """
        Supprime un client par son ID
        
        Args:
            client_id: L'ID du client à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if client_id in self._clients:
            del self._clients[client_id]
            return True
        return False

    def find_by_name(self, nom: str, prenom: Optional[str] = None) -> List[Client]:
        """
        Recherche des clients par nom et prénom optionnel
        
        Args:
            nom: Le nom à rechercher
            prenom: Le prénom à rechercher (optionnel)
            
        Returns:
            Une liste des clients correspondant aux critères
        """
        results = []
        for client in self._clients.values():
            if client.nom.lower() == nom.lower():
                if prenom is None or client.prenom.lower() == prenom.lower():
                    results.append(client)
        return results
    
    def find_by_permis(self, permis: str) -> Optional[Client]:
        """
        Recherche un client par son numéro de permis
        
        Args:
            permis: Le numéro de permis à rechercher
            
        Returns:
            Le client correspondant ou None
        """
        for client in self._clients.values():
            if client.permis == permis:
                return client
        return None
    
    def find_by_email(self, email: str) -> Optional[Client]:
        """
        Recherche un client par son email
        
        Args:
            email: L'email à rechercher
            
        Returns:
            Le client correspondant ou None
        """
        for client in self._clients.values():
            if client.email.lower() == email.lower():
                return client
        return None
    
    def find_with_active_rentals(self) -> List[Client]:
        """
        Recherche tous les clients ayant au moins une location active
        
        Returns:
            Liste des clients avec des locations actives
        """
        return [client for client in self._clients.values() if client.historique_locations]

    def create_client(self, nom: str, prenom: str, permis: str, telephone: str, email: str, voitureLouer=None) -> Client:
        """
        Crée un nouveau client et l'ajoute au repository
        
        Args:
            nom: Nom du client
            prenom: Prénom du client
            permis: Numéro de permis du client
            telephone: Numéro de téléphone du client
            email: Email du client
            voitureLouer: Voiture éventuellement louée
            
        Returns:
            Le client créé
        """
        client = Client(nom, prenom, permis, telephone, email, voitureLouer)
        self.save(client)
        return client