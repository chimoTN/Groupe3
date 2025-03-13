import pytest

from ..lib.application.use_cases.ProposerDevisUseCase import ProposerDevisUseCase
from ..lib.application.exceptions import PrixDevisInvalideException, VehiculeIntrouvableException
from ..lib.domain.vehicule import Vehicule
from ..lib.domain.immatriculation import Immatriculation

@pytest.fixture
def devisUseCase():
    return ProposerDevisUseCase()

@pytest.fixture
def vehicule():
    immatriculation = Immatriculation(identifiant="AA-123-AA", departement="AA")
    return Vehicule(
        marque="marque",
        modele="modele",
        annee=1980,
        immatriculation=immatriculation,
        kilometrage=1000,
        prix_journalier=50.0,
        etat="etat",
        typeVehicule="voiture"
    )

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
