import unittest
from unittest.mock import ANY, MagicMock
from decimal import Decimal

from ..lib.application.use_cases.restitutionVehicule import RestitutionVehicule
from ..lib.domain.client import Client
from ..lib.domain.vehicule import Vehicule
from ..lib.domain.contratLocation import ContratLocation
from ..lib.repositories.contratRepository import ContratRepository
from ..lib.application.ClientRepositoryPort import ClientRepositoryPort
from ..lib.application.VehiculeRepositoryPort import VehiculeRepositoryPort
from ..lib.application.use_cases.restitutionVehicule import RestitutionVehicule

class TestRestitutionVehicule(unittest.TestCase):

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        Création des mocks et initialisation du use case.
        """

        self.mock_client_repo = MagicMock(spec=ClientRepositoryPort)
        self.mock_vehicule_repo = MagicMock(spec=VehiculeRepositoryPort)
        self.mock_contrat_repo = MagicMock(spec=ContratRepository)

        self.use_case = RestitutionVehicule(
            client_repository=self.mock_client_repo,
            vehicule_repository=self.mock_vehicule_repo,
            contrat_repository=self.mock_contrat_repo
        )
        
        self.client = MagicMock(spec=Client)
        self.client.id = 1
        self.client.nom = "Doe"
        self.client.prenom = "John"
        self.client.historique_locations = []

        self.vehicule = MagicMock(spec=Vehicule)
        self.vehicule.id = 10
        self.vehicule.marque = "Peugeot"
        self.vehicule.modele = "208"
        self.vehicule.kilometrage = 25000
        self.vehicule.defauts = []
        self.vehicule.etat = "Nickel"

        self.contrat = MagicMock(spec=ContratLocation)
        self.contrat.getId.return_value = 100
        self.contrat.getClient.return_value = self.client
        self.contrat.getVehicule.return_value = self.vehicule
        self.contrat.getCaution.return_value = 1000.0
        self.contrat.getDefautsInitiaux.return_value = []
        
        self.mock_client_repo.get_by_id.return_value = self.client
        self.mock_vehicule_repo.get_by_id.return_value = self.vehicule
        self.mock_contrat_repo.trouver_contrat_actif.return_value = self.contrat
        
        self.client.historique_locations.append(self.vehicule)

    def test_restitution_sans_nouveaux_defauts(self):
        """
        Test de restitution sans nouveaux défauts.
        La caution ne doit pas être retenue.
        """
        self.contrat.enregistrerRestitution.return_value = 0.0
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=300,
            etat_restitution="Nickel",
            defauts_restitution=[]
        )
        
        self.assertIsNotNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 0.0)
        
        self.contrat.enregistrerRestitution.assert_called_once()
        self.vehicule.retourner.assert_called_once_with(300, "Nickel", [])
        self.mock_client_repo.save.assert_called_once_with(self.client)
        self.mock_vehicule_repo.save.assert_called_once_with(self.vehicule)
        self.mock_contrat_repo.save.assert_called_once_with(self.contrat)
    
    def test_restitution_avec_nouveaux_defauts(self):
        """
        Test de restitution avec de nouveaux défauts.
        Une partie de la caution doit être retenue.
        """
        self.contrat.enregistrerRestitution.return_value = Decimal('200.00')
        
        nouveaux_defauts = ["Rayure portière gauche", "Phare avant droit cassé"]
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=300,
            etat_restitution="Endommagé",
            defauts_restitution=nouveaux_defauts
        )
        
        self.assertIsNotNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 200.0)
        
        self.contrat.enregistrerRestitution.assert_called_once()
        self.vehicule.retourner.assert_called_once_with(300, caution., nouveaux_defauts)
        self.mock_client_repo.save.assert_called_once_with(self.client)
        self.mock_vehicule_repo.save.assert_called_once_with(self.vehicule)
        self.mock_contrat_repo.save.assert_called_once_with(self.contrat)
    
    def test_restitution_vehicule_vole(self):
        """
        Test de restitution d'un véhicule volé.
        La caution doit être entièrement retenue.
        """
        self.contrat.enregistrerRestitution.return_value = Decimal('1000.00')
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=0,  
            etat_restitution="Volé",
            defauts_restitution=["Véhicule volé"]
        )
        
        self.assertIsNotNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 1000.0)
        
        self.contrat.enregistrerRestitution.assert_called_once()
        self.vehicule.retourner.assert_called_once()
    
    def test_restitution_avec_defauts_preexistants(self):
        """
        Test de restitution avec des défauts qui existaient déjà lors de la signature.
        La caution ne doit pas être retenue pour ces défauts.
        """
        defauts_initiaux = ["Rayure pare-chocs arrière", "Siège arrière taché"]
        
        defauts_restitution = ["Rayure pare-chocs arrière", "Siège arrière taché", "Rétroviseur gauche cassé"]
        
        self.contrat.getDefautsInitiaux.return_value = defauts_initiaux
        self.contrat.enregistrerRestitution.return_value = Decimal('100.00')
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=200,
            etat_restitution="Endommagé",
            defauts_restitution=defauts_restitution
        )
        
        self.assertIsNotNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 100.0) 
        
        self.contrat.enregistrerRestitution.assert_called_once()
        
        self.contrat.enregistrerRestitution.assert_called_with(
            date_restitution=ANY,
            km_retour=ANY,
            defauts_restitution=defauts_restitution
        )
    
    def test_restitution_client_inexistant(self):
        """Test de restitution avec un client inexistant"""
        self.mock_client_repo.get_by_id.return_value = None
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=999,
            vehicule_id=10,
            km_parcourus=100,
            etat_restitution="Nickel"
        )
        
        self.assertIsNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 0.0)
    
    def test_restitution_vehicule_inexistant(self):
        """Test de restitution avec un véhicule inexistant"""
        self.mock_vehicule_repo.get_by_id.return_value = None
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=999,
            km_parcourus=100,
            etat_restitution="Nickel"
        )
        
        self.assertIsNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 0.0)
    
    def test_restitution_sans_contrat_actif(self):
        """Test de restitution sans contrat actif"""
        self.mock_contrat_repo.trouver_contrat_actif.return_value = None
        
        vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=100,
            etat_restitution="Nickel"
        )
        
        self.assertIsNone(vehicule_restitue)
        self.assertEqual(caution_retenue, 0.0)
    
    def test_restitution_avec_exception_dans_contrat(self):
        """Test de gestion des exceptions lors de l'enregistrement de la restitution"""
        self.contrat.enregistrerRestitution.side_effect = ValueError("Erreur test")
        
        try:
            vehicule_restitue, caution_retenue = self.use_case.restituer_vehicule(
                client_id=1,
                vehicule_id=10,
                km_parcourus=100,
                etat_restitution="Nickel"
            )
            self.fail("Une exception aurait dû être levée")
            
        except ValueError:
            pass
        
        self.mock_client_repo.save.assert_not_called()
        self.mock_vehicule_repo.save.assert_not_called()
        self.mock_contrat_repo.save.assert_not_called()

if __name__ == '__main__':
    unittest.main()