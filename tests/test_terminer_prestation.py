import pytest

from ..lib.application.use_cases.TerminerPrestationUseCase import TerminerPrestationUseCase, DevisIntrouvable
from ..lib.domain.vehicule import Vehicule
from ..lib.domain.devis import Devis

@pytest.fixture
def prestationUseCase():
    return TerminerPrestationUseCase()

@pytest.fixture
def vehicule():
    return Vehicule("marque", "modele", 1980, "aa-123-aa", 1000, 50.0, "etat", "voiture")

@pytest.fixture
def devis(vehicule):
    return Devis(vehicule, 10000)

def test_terminer_prestation_use_case_invalid_devis(prestationUseCase):
    devis = None
    with pytest.raises(DevisIntrouvable):
        prestationUseCase.terminerPrestation(devis)

def test_realiser_prestation_valid(prestationUseCase, devis):
    prestation = prestationUseCase.terminerPrestation(devis)
