import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.repositories.clientRepository import ClientRepository

from ..lib.repositories.vehiculeRepository import VehiculeRepository
from ..lib.use_cases.locationVehicule.restitutionVehicule import RestitutionVehicule


class TestRestitutionVoiture(unittest.TestCase):
    
    def setUp(self):
        self.client_repo = MagicMock(spec=ClientRepository)
        self.vehicule_repo = MagicMock(spec=VehiculeRepository)
        
        self.client = MagicMock()
        self.client.id = 1
        self.client.nom = "Dupont"
        self.client.prenom = "Jean"
        self.client.historique_locations = []
        
        self.vehicule = MagicMock()
        self.vehicule.id = 1
        self.vehicule.marque = "Peugeot"
        self.vehicule.modele = "208"
        self.vehicule.immatriculation = "AB-123-CD"
        self.vehicule.kilometrage = 25000
        self.vehicule.prix_journalier = 45.0
        self.vehicule.disponible = False
        self.vehicule.etat = "Bon"
        
        self.client_repo.get_by_id.return_value = self.client
        self.vehicule_repo.get_by_id.return_value = self.vehicule
        
        self.client.historique_locations.append(self.vehicule)
    
    def test_restitution_normale(self):
        RestitutionVehicule(self.client.id, self.vehicule.id, 300, "Propre")
        self.client.historique_locations.remove.assert_called_with(self.vehicule)
        self.vehicule.retourner.assert_called_with(300, "Propre")
    
    def test_restitution_voiture_sale(self):
        RestitutionVehicule(self.client.id, self.vehicule.id, 300, "Sale")
        self.client.historique_locations.remove.assert_called_with(self.vehicule)
        self.vehicule.retourner.assert_called_with(300, "Sale")
    
    def test_restitution_voiture_cassee(self):
        RestitutionVehicule(self.client.id, self.vehicule.id, 300, "Cassé")
        self.client.historique_locations.remove.assert_called_with(self.vehicule)
        self.vehicule.retourner.assert_called_with(300, "Cassé")
    
    def test_non_restitution_voiture(self):
        RestitutionVehicule(self.client.id, self.vehicule.id, 0, "Non Rendu")
        self.client.historique_locations.remove.assert_not_called()
        self.vehicule.retourner.assert_not_called()
    
    def test_client_inexistant(self):
        self.client_repo.get_by_id.return_value = None
        RestitutionVehicule(999, self.vehicule.id, 300, "Propre")
        self.client_repo.get_by_id.assert_called_with(999)
    
    def test_vehicule_inexistant(self):
        self.vehicule_repo.get_by_id.return_value = None
        RestitutionVehicule(self.client.id, 999, 300, "Propre")
        self.vehicule_repo.get_by_id.assert_called_with(999)
    
    def test_client_n_a_pas_loue_ce_vehicule(self):
        autre_client = MagicMock()
        autre_client.id = 2
        autre_client.nom = "Martin"
        autre_client.prenom = "Paul"
        autre_client.historique_locations = []
        
        self.client_repo.get_by_id.return_value = autre_client
        RestitutionVehicule(autre_client.id, self.vehicule.id, 300, "Propre")
        autre_client.historique_locations.remove.assert_not_called()
        self.vehicule.retourner.assert_not_called()

if __name__ == "__main__":
    unittest.main()