import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.repositories.clientRepository import ClientRepository

from ..lib.repositories.vehiculeRepository import VehiculeRepository
from ..lib.use_cases.locationVehicule.restitutionVehicule import RestitutionVehicule


from ..lib.entities.client import Client
from ..lib.entities.vehicule import Vehicule

class TestRestitutionVoiture(unittest.TestCase):

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        On y crée des mocks pour les repositories et on instancie le use case.
        """
        self.mock_client_repo = MagicMock()
        self.mock_vehicule_repo = MagicMock()

        # Instanciation du use case avec les mocks
        self.use_case = RestitutionVehicule(
            client_repository=self.mock_client_repo,
            vehicule_repository=self.mock_vehicule_repo
        )
        
        # Création d'objets Client et Vehicule factices
        self.client = Client(
            nom="Doe", 
            prenom="John", 
            permis="123ABC", 
            telephone="0123456789", 
            email="john.doe@email",
            voitureLouer=None
        )
        self.vehicule = Vehicule(
            marque="Peugeot", 
            modele="208", 
            annee=2021, 
            immatriculation="AB-123-CD", 
            kilometrage=25000, 
            prix_journalier=45.0,
            etat="Nickel", 
            typeVehicule="Citadine"
        )

        # On simule l'ajout du véhicule dans l'historique de location du client
        self.client.historique_locations.append(self.vehicule)

        # On prépare le mock : quand on appelle get_by_id, il renvoie notre client/vehicule
        self.mock_client_repo.get_by_id.return_value = self.client
        self.mock_vehicule_repo.get_by_id.return_value = self.vehicule

    def test_restituer_vehicule_nickel(self):
        """
        Test de restitution avec un état 'nickel'.
        On s'attend à ce que le véhicule soit rendu disponible et son kilométrage mis à jour.
        """
        nouveau_km = 300
        etat = "nickel"

        # Appel au use case
        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=nouveau_km,
            etat_restitution=etat
        )

        # Vérifications
        self.assertIsNotNone(result)
        self.assertEqual(result.etat, "Nickel")
        self.assertEqual(result.kilometrage, 25000 + nouveau_km)
        self.assertTrue(result.disponible)
        self.assertNotIn(self.vehicule, self.client.historique_locations)

        # Vérifie qu'on a bien sauvegardé les modifications
        self.mock_vehicule_repo.save.assert_called_once_with(self.vehicule)
        self.mock_client_repo.save.assert_called_once_with(self.client)

    def test_restituer_vehicule_sale(self):
        """
        Test de restitution avec un état 'sale'.
        """
        nouveau_km = 100
        etat = "sale"

        # Appel au use case
        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=nouveau_km,
            etat_restitution=etat
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.etat, "Sale")
        self.assertEqual(result.kilometrage, 25000 + nouveau_km)
        self.assertTrue(result.disponible)
        self.assertNotIn(self.vehicule, self.client.historique_locations)

    def test_restituer_vehicule_endommage(self):
        """
        Test de restitution avec un état 'endommagé'.
        """
        nouveau_km = 50
        etat = "endommagé"

        # Appel
        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=nouveau_km,
            etat_restitution=etat
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.etat, "Endommagé")
        self.assertEqual(result.kilometrage, 25000 + nouveau_km)
        self.assertTrue(result.disponible)
        self.assertNotIn(self.vehicule, self.client.historique_locations)

    def test_restituer_vehicule_vole(self):
        """
        Test de restitution avec un état 'volé'.
        Dans l'exemple : on choisit de rendre le véhicule indisponible.
        """
        # On peut ajuster la logique si, par exemple, vous préférez 
        # laisser le véhicule indisponible quand il est volé.
        # Adaptez en fonction de votre logique métier !
        nouveau_km = 10
        etat = "volé"

        # Appel
        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=nouveau_km,
            etat_restitution=etat
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.etat, "Volé")
        self.assertEqual(result.kilometrage, 25000 + nouveau_km)

        # Si la logique code "volé" met disponible = False :
        # self.assertFalse(result.disponible) 
        # OU si vous laissez la disponibilité telle quelle, ajustez le test.
        self.assertNotIn(self.vehicule, self.client.historique_locations)

    def test_restituer_vehicule_client_inexistant(self):
        """
        Cas où le client_id n'est pas trouvé dans le repository
        => On s'attend à obtenir None
        """
        self.mock_client_repo.get_by_id.return_value = None

        result = self.use_case.restituer_vehicule(
            client_id=999, 
            vehicule_id=10,
            km_parcourus=50,
            etat_restitution="nickel"
        )
        self.assertIsNone(result)

    def test_restituer_vehicule_non_trouve(self):
        """
        Cas où le vehicule_id n'est pas trouvé dans le repository
        => On s'attend à obtenir None
        """
        self.mock_vehicule_repo.get_by_id.return_value = None

        result = self.use_case.restituer_vehicule(
            client_id=1, 
            vehicule_id=999,
            km_parcourus=50,
            etat_restitution="nickel"
        )
        self.assertIsNone(result)

    def test_restituer_vehicule_non_loue_par_ce_client(self):
        """
        Cas où le véhicule n'est pas dans l'historique_locations du client.
        => On s'attend à obtenir None
        """
        # On vide l'historique de locations pour simuler
        self.client.historique_locations.clear()

        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=50,
            etat_restitution="nickel"
        )
        self.assertIsNone(result)

    def test_restituer_vehicule_etat_inconnu(self):
        """
        Cas où l'état transmis ne correspond pas à "nickel", "sale", "endommagé", ou "volé".
        => On s'attend à obtenir None
        """
        result = self.use_case.restituer_vehicule(
            client_id=1,
            vehicule_id=10,
            km_parcourus=50,
            etat_restitution="bizarre"  # état inconnu
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
