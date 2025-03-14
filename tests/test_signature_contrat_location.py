import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock
from contextlib import contextmanager
from decimal import Decimal 

from lib.application.use_cases.signerContratDeLocation import SignerContratDeLocation
from lib.application.exceptions import (
    AssuranceInexistanteException, ClientInexistantException, ContratLocationException, DateInvalideException,
    EnregistrementContratException, VehiculeInexistantException, VehiculeNonDisponibleException, DevisIntrouvable, PrixDevisInvalideException, VehiculeIntrouvableException
)

@contextmanager
def patch_singleton_repositories(mock_repos):
    """
    Gestionnaire de contexte pour patcher les repositories singleton
    """
    with patch('lib.repositories.clientRepository.ClientRepository._instance', mock_repos['client']), \
         patch('lib.repositories.vehiculeRepository.VehiculeRepository._instance', mock_repos['vehicule']), \
         patch('lib.repositories.assuranceRepository.AssuranceRepository._instance', mock_repos['assurance']), \
         patch('lib.repositories.contratRepository.ContratRepository._instance', mock_repos['contrat']), \
         patch('builtins.print'):
        yield

@pytest.fixture
def mock_repositories():
    """Fixture pour créer des mocks des repositories."""
    client_repo_mock = MagicMock()
    vehicule_repo_mock = MagicMock()
    assurance_repo_mock = MagicMock()
    contrat_repo_mock = MagicMock()
    
    client_repo_mock.get_by_id.return_value = MagicMock(
        getNom=lambda: "Doe", 
        getPrenom=lambda: "John",
        id=1
    )
    
    vehicule_repo_mock.get_by_id.return_value = MagicMock(
        getMarque=lambda: "Peugeot", 
        getModele=lambda: "208",
        id=2
    )
    vehicule_repo_mock.is_available_between.return_value = True
    vehicule_repo_mock.calculate_rental_cost.return_value = Decimal('350.0')
    
    assurance_repo_mock.get_by_id.return_value = MagicMock(
        getNom=lambda: "Assurance Premium", 
        getTarif=lambda: Decimal('10.0'), 
        id=3
    )
    
    contrat_repo_mock.save.return_value = 1 
    
    return {
        'client': client_repo_mock,
        'vehicule': vehicule_repo_mock,
        'assurance': assurance_repo_mock,
        'contrat': contrat_repo_mock
    }

@pytest.fixture
def future_date():
    """Fixture pour fournir une date future, utile pour les tests."""
    return date.today() + timedelta(days=30)

def test_signer_contrat_success(mock_repositories, future_date):
    """Test du cas de succès pour la signature de contrat"""
    with patch_singleton_repositories(mock_repositories):
        contrat = SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=7
        )
        
        assert contrat is not None
        mock_repositories['client'].get_by_id.assert_called_once_with(1)
        mock_repositories['vehicule'].get_by_id.assert_called_once_with(2)
        mock_repositories['vehicule'].is_available_between.assert_called_once()
        mock_repositories['assurance'].get_by_id.assert_called_once_with(3)
        mock_repositories['contrat'].save.assert_called_once()
        mock_repositories['vehicule'].set_availability.assert_called_once_with(2, False)

def test_client_inexistant(mock_repositories, future_date):
    """Test avec un client inexistant"""
    mock_repositories['client'].get_by_id.return_value = None
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(ClientInexistantException):
        SignerContratDeLocation.main(
            client_id=999, 
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=7
        )

def test_vehicule_inexistant(mock_repositories, future_date):
    """Test avec un véhicule inexistant"""
    mock_repositories['vehicule'].get_by_id.return_value = None
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(VehiculeInexistantException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=999, 
            assurance_id=3,
            date_debut=future_date,
            duree=7
        )

def test_assurance_inexistante(mock_repositories, future_date):
    """Test avec une assurance inexistante"""
    mock_repositories['assurance'].get_by_id.return_value = None
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(AssuranceInexistanteException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=999,
            date_debut=future_date,
            duree=7
        )

def test_vehicule_non_disponible(mock_repositories, future_date):
    """Test avec un véhicule non disponible"""
    mock_repositories['vehicule'].is_available_between.return_value = False
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(VehiculeNonDisponibleException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=7
        )

def test_date_dans_passe(mock_repositories):
    """Test avec une date dans le passé"""
    date_passee = date.today() - timedelta(days=1)
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(DateInvalideException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=date_passee,
            duree=7
        )

def test_duree_invalide(mock_repositories, future_date):
    """Test avec une durée invalide (négative ou nulle)"""
    with patch_singleton_repositories(mock_repositories), pytest.raises(DateInvalideException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=0  
        )

def test_sans_assurance(mock_repositories, future_date):
    """Test sans assurance (paramètre optionnel)"""
    with patch_singleton_repositories(mock_repositories):
        contrat = SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=None, 
            date_debut=future_date,
            duree=7
        )
        
        assert contrat is not None
        mock_repositories['assurance'].get_by_id.assert_not_called()

def test_erreur_enregistrement_contrat(mock_repositories, future_date):
    """Test de l'échec de l'enregistrement du contrat"""
    mock_repositories['contrat'].save.side_effect = Exception("Erreur de base de données")
    
    with patch_singleton_repositories(mock_repositories), pytest.raises(EnregistrementContratException):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=7
        )

def test_calcul_cout_avec_assurance(mock_repositories, future_date):
    """Test que le coût inclut bien l'assurance"""

    vehicule_tarif = Decimal('50.0')
    assurance_tarif = Decimal('10.0')
    duree = 7
    vehicule_cout_total = vehicule_tarif * duree
    assurance_cout_total = assurance_tarif * duree
    cout_total = vehicule_cout_total + assurance_cout_total
    
    mock_repositories['vehicule'].calculate_rental_cost.return_value = vehicule_cout_total
    mock_repositories['assurance'].get_by_id.return_value = MagicMock(
        getNom=lambda: "Assurance Premium",
        getTarif=lambda: assurance_tarif,
        id=3
    )
    
    with patch_singleton_repositories(mock_repositories):
        contrat = SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=duree
        )
        

        assert contrat.getCout() == cout_total

def test_calcul_cout_sans_assurance(mock_repositories, future_date):
    """Test que le coût est correctement calculé sans assurance"""

    vehicule_tarif = Decimal('50.0')
    duree = 7
    vehicule_cout_total = vehicule_tarif * duree
    
#     mock_repositories['vehicule'].calculate_rental_cost.return_value = vehicule_cout_total
    
    with patch_singleton_repositories(mock_repositories):
        contrat = SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=None,
            date_debut=future_date,
            duree=duree
        )
        

        assert contrat.getCout() == vehicule_cout_total

def test_avec_defauts_initiaux(mock_repositories, future_date):
    """Test avec des défauts initiaux spécifiés"""
    defauts = ["Rayure portière", "Phare cassé"]
    
    with patch_singleton_repositories(mock_repositories):
        contrat = SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            assurance_id=3,
            date_debut=future_date,
            duree=7,
            defauts_initiaux=defauts
        )
        
        assert contrat.getDefautsInitiaux() == defauts
