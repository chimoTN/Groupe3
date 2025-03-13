import pytest

from ..lib.application.use_cases import RealiserPrestationUseCase
from ..lib.application.exceptions import DevisIntrouvable
from ..lib.domain.vehicule import Vehicule
from ..lib.domain.devis import Devis

@pytest.fixture
def prestationUseCase():
    return RealiserPrestationUseCase()

@pytest.fixture
def vehicule():
    return Vehicule("marque", "modele", 1980, "aa-123-aa", 1000, 50.0, "etat", "voiture")

@pytest.fixture
def devis(vehicule):
    return Devis(vehicule, 10000)

def test_realiser_prestation_use_case_invalid_devis(prestationUseCase):
    devis = None
    with pytest.raises(DevisIntrouvable):
        prestationUseCase.realiserPrestation(devis)

def test_realiser_prestation_valid(prestationUseCase, devis):
    prestation = prestationUseCase.realiserPrestation(devis)
