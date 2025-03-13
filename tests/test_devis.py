import pytest

from ..lib.application.use_cases import ProposerDevisUseCase
from ..lib.application.exceptions import PrixDevisInvalideException, VehiculeIntrouvableException
from ..lib.domain.vehicule import Vehicule

@pytest.fixture
def devisUseCase():
    return ProposerDevisUseCase()

@pytest.fixture
def vehicule():
    return Vehicule("marque", "modele", 1980, "aa-123-aa", 1000, 50.0, "etat", "voiture")

def test_devis_use_case_invalid_price(devisUseCase, vehicule):
    prix = -5
    with pytest.raises(PrixDevisInvalideException):
        devisUseCase.proposerDevis(vehicule, prix)

def test_devis_use_case_invalid_vehicule(devisUseCase):
    vehicule = None
    prix = 10000
    with pytest.raises(VehiculeIntrouvableException):
        devisUseCase.proposerDevis(vehicule, prix)

def test_devis_valid(devisUseCase, vehicule):
    prix = 10000
    devis = devisUseCase.proposerDevis(vehicule, prix)
    assert devis.vehicule == vehicule
    assert devis.prix == prix
