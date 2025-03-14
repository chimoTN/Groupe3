import pytest

from ..lib.application.use_cases.ProposerDevisUseCase import ProposerDevisUseCase
from ..lib.application.exceptions import PrixDevisInvalideException, VehiculeIntrouvableException
from ..lib.domain.devis import Devis
from ..lib.domain.vehicule import Vehicule
from ..lib.domain.immatriculation import Immatriculation
from ..lib.infrastructure.InMemoryDevisRepository import InMemoryDevisRepository
from ..lib.infrastructure.InMemoryVehiculeRepository import InMemoryVehiculeRepository

@pytest.fixture
def devisUseCase():
    use_case = ProposerDevisUseCase()
    return use_case

@pytest.fixture
def vehiculeRepository():
    repo = InMemoryVehiculeRepository()
    repo._initialize()
    return repo

@pytest.fixture
def devisRepository():
    repo = InMemoryDevisRepository()
    repo._initialize()
    return repo

@pytest.fixture
def vehicule():
    immatriculation = Immatriculation(identifiant="AA-123-AA", departement="78")
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

def test_devis_created(devisUseCase, vehicule, vehiculeRepository, devisRepository):
    prix = 10000
    devisUseCase.proposerDevis(vehicule, prix) 
       
    assert len(vehiculeRepository.get_all()) == 1
    assert len(devisRepository.get_all()) == 1

def test_repository_empty_on_creation(devisRepository):
    assert len(devisRepository.get_all()) == 0

def test_repository_clear(devisRepository, vehicule):
    devisRepository.save(Devis(vehicule, prix=10.0))
    devisRepository.clear()
    assert len(devisRepository.get_all()) == 0

def test_repository_delete_devis(devisRepository, vehicule):
    devis = Devis(vehicule, prix=10.0)
    devisRepository.save(devis)
    devisRepository.delete(devis)

    assert len(devisRepository.get_all()) == 0
