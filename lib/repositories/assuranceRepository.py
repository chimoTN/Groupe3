from typing import Optional, List
from lib.entities.assurance import Assurance

class AssuranceRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssuranceRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialise les données du repository lors de la première création"""
        # Simulation d'une base de données avec une liste d'assurances
        self._assurances = {}
        self._next_id = 1

    def get_by_id(self, assurance_id: int) -> Optional[Assurance]:
        """
        Récupère une assurance par son ID
        
        Args:
            assurance_id: L'ID de l'assurance à récupérer
            
        Returns:
            L'assurance correspondante, ou None si elle n'existe pas
        """
        return self._assurances.get(assurance_id)

    def get_all(self) -> List[Assurance]:
        """
        Récupère toutes les assurances
        
        Returns:
            Une liste de toutes les assurances
        """
        return list(self._assurances.values())

    def save(self, assurance: Assurance) -> int:
        """
        Sauvegarde une assurance (création ou mise à jour)
        
        Args:
            assurance: L'assurance à sauvegarder
            
        Returns:
            L'ID de l'assurance
        """
        # Vérifier si l'assurance a déjà un ID
        if not hasattr(assurance, 'id') or assurance.id is None:
            assurance.id = self._next_id
            self._next_id += 1
        
        # Sauvegarder ou mettre à jour l'assurance
        self._assurances[assurance.id] = assurance
        return assurance.id

    def delete(self, assurance_id: int) -> bool:
        """
        Supprime une assurance par son ID
        
        Args:
            assurance_id: L'ID de l'assurance à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if assurance_id in self._assurances:
            del self._assurances[assurance_id]
            return True
        return False

    def find_by_name(self, nom: str) -> List[Assurance]:
        """
        Recherche des assurances par nom
        
        Args:
            nom: Le nom à rechercher
            
        Returns:
            Une liste des assurances correspondant au critère
        """
        return [a for a in self._assurances.values() if nom.lower() in a.nom.lower()]
    
    def create_assurance(self, nom: str) -> Assurance:
        """
        Crée une nouvelle assurance et l'ajoute au repository
        
        Args:
            nom: Nom de l'assurance
            
        Returns:
            L'assurance créée
        """
        assurance = Assurance(nom)
        self.save(assurance)
        return assurance