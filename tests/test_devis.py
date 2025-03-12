import unittest
import pytest

from ..lib.use_cases.proposerDevis import ProposerDevisUseCase, InvalidDevisPriceException
from ..lib.entities.vehicule import Vehicule

@pytest.fixture
def devisUseCase():
    return ProposerDevisUseCase()

@pytest.fixture
def vehicule():
    return Vehicule("marque", "modele", 1980, "aa-123-aa", 1000, 50.0, "etat", "voiture")

class TestDevisUseCase(unittest.TestCase):
    # def test_devis_use_case(self, devisUseCase: ProposerDevisUseCase):
        # self.assertEqual(1, 1)

    def test_devis_use_case_invalid_price(self, vehicule, devisUseCase):
        prix = -5
        self.assertRaises(InvalidDevisPriceException, devisUseCase.ProposerDevis(vehicule, prix))
    
    def test_devis_use_case_invalid_vehicule(self):
        vehicule = None
        prix = 10000
        with self.assertRaises(Exception):
            ProposerDevisUseCase.ProposerDevis(vehicule, prix)
    
