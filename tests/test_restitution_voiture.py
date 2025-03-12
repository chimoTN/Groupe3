import unittest

from lib.entities.client import Client
from lib.entities.vehicule import Vehicule

class TestRestitutionVoiture(unittest.TestCase):

    def setUp(self):
        """Initialisation des objets avant chaque test."""
        self.client = Client("Dupont", "Jean", "123456789", "0601020304", "jean.dupont@email.com", None)
        self.voiture = Vehicule("Peugeot", "208", 2021, "AB-123-CD", 25000, 45.0, "Bon état", "Voiture")

    # Un client rend un véhicule en bon état
    def test_rendre_vehicule_nickel(self):
        self.client.louer_voiture(self.voiture)  
        self.client.retourner_voiture(self.voiture, 100, "Nickel")

        self.assertTrue(self.voiture.disponible)
        self.assertEqual(self.voiture.kilometrage, 25100)
        self.assertEqual(self.voiture.etat, "Nickel")

    # Un client rend un véhicule sale
    def test_rendre_vehicule_sale(self):
        self.client.louer_voiture(self.voiture)
        self.client.retourner_voiture(self.voiture, 150, "Sale")

        self.assertTrue(self.voiture.disponible)
        self.assertEqual(self.voiture.kilometrage, 25150)
        self.assertEqual(self.voiture.etat, "Sale")

    # Un client rend un véhicule endommagé
    def test_rendre_vehicule_endomager(self):
        self.client.louer_voiture(self.voiture)
        self.client.retourner_voiture(self.voiture, 200, "Endommagé")

        self.assertTrue(self.voiture.disponible)
        self.assertEqual(self.voiture.kilometrage, 25200)
        self.assertEqual(self.voiture.etat, "Endommagé")

    # Un client tente de rendre un véhicule qu'il n'a pas loué
    def test_vehicule_non_rendu(self):
        autre_voiture = Vehicule("Renault", "Clio", 2020, "BC-234-DE", 30000, 40.0, "Bon état", "Voiture")
        
        with self.assertLogs("client", level="WARNING") as log:
            self.client.retourner_voiture(autre_voiture, 50)
            self.assertIn("n'a pas cette voiture en location", log.output[0])

        self.assertTrue(autre_voiture.disponible)
        self.assertEqual(autre_voiture.kilometrage, 30000)

if __name__ == '__main__':
    unittest.main()
