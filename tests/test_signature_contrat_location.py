import sys
import os
from pathlib import Path
import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

# Ajouter le chemin racine au PYTHONPATH
root_dir = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, root_dir)
print(f"Added {root_dir} to Python path")

# Importer le module signerContratDeLocation avec ses classes et exceptions
from lib.use_cases.locationVehicule.signerContratDeLocation import (
    SignerContratDeLocation,
    ClientInexistantError,
    VehiculeInexistantError,
    AssuranceInexistanteError,
    VehiculeNonDisponibleError,
    DateInvalideError,
    ContratLocationError
)

# Fixtures pour les mocks
@pytest.fixture
def mock_repositories():
    """Configure les repositories mockés pour les tests"""
    # Créer les mocks
    client_repo = MagicMock()
    vehicule_repo = MagicMock()
    assurance_repo = MagicMock()
    contrat_repo = MagicMock()
    
    # Valeurs de retour par défaut
    client_repo.get_by_id.return_value = MagicMock(getNom=lambda: "Dupont", getPrenom=lambda: "Jean")
    vehicule_repo.get_by_id.return_value = MagicMock(getMarque=lambda: "Renault", getModele=lambda: "Clio")
    vehicule_repo.is_available_between.return_value = True
    vehicule_repo.calculate_rental_cost.return_value = 350.0  # 50€/jour pour 7 jours
    assurance_repo.get_by_id.return_value = MagicMock(getTarif=lambda: 10.0)
    contrat_repo.save.return_value = 123  # ID du contrat
    
    # Patch les constructeurs des repositories
    with patch('lib.use_cases.locationVehicule.signerContratDeLocation.ClientRepository', return_value=client_repo), \
         patch('lib.use_cases.locationVehicule.signerContratDeLocation.VehiculeRepository', return_value=vehicule_repo), \
         patch('lib.use_cases.locationVehicule.signerContratDeLocation.AssuranceRepository', return_value=assurance_repo), \
         patch('lib.use_cases.locationVehicule.signerContratDeLocation.ContratRepository', return_value=contrat_repo):
        
        yield {
            'client': client_repo,
            'vehicule': vehicule_repo,
            'assurance': assurance_repo,
            'contrat': contrat_repo
        }

@pytest.fixture
def future_date():
    """Renvoie une date dans le futur pour les tests"""
    return date.today() + timedelta(days=1)


# Tests pour la fonction SignerContratDeLocation.main
def test_signer_contrat_success(mock_repositories, future_date):
    """Test du cas de succès pour la signature de contrat"""
    # Test avec les paramètres valides
    contrat = SignerContratDeLocation.main(
        client_id=1,
        vehicule_id=2,
        date_debut=future_date,
        duree=7,
        assurance_id=3
    )
    
    # Vérifier que le contrat a été créé correctement
    assert contrat is not None
    assert hasattr(contrat, 'id')
    assert contrat.id == 123
    
    # Vérifier que les repositories ont été appelés correctement
    mock_repositories['client'].get_by_id.assert_called_once_with(1)
    mock_repositories['vehicule'].get_by_id.assert_called_once_with(2)
    mock_repositories['assurance'].get_by_id.assert_called_once_with(3)
    mock_repositories['vehicule'].is_available_between.assert_called_once()
    mock_repositories['contrat'].save.assert_called_once()
    mock_repositories['vehicule'].set_availability.assert_called_once_with(2, False)


def test_client_inexistant(mock_repositories, future_date):
    """Test de l'absence de client"""
    # Modifier le mock pour que le client n'existe pas
    mock_repositories['client'].get_by_id.return_value = None
    
    # Vérifier que l'exception est levée
    with pytest.raises(ClientInexistantError):
        SignerContratDeLocation.main(
            client_id=999,  # ID de client inexistant
            vehicule_id=2,
            date_debut=future_date,
            duree=7,
            assurance_id=3
        )


def test_vehicule_inexistant(mock_repositories, future_date):
    """Test de l'absence de véhicule"""
    # Modifier le mock pour que le véhicule n'existe pas
    mock_repositories['vehicule'].get_by_id.return_value = None
    
    # Vérifier que l'exception est levée
    with pytest.raises(VehiculeInexistantError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=999,  # ID de véhicule inexistant
            date_debut=future_date,
            duree=7,
            assurance_id=3
        )


def test_assurance_inexistante(mock_repositories, future_date):
    """Test de l'absence d'assurance"""
    # Modifier le mock pour que l'assurance n'existe pas
    mock_repositories['assurance'].get_by_id.return_value = None
    
    # Vérifier que l'exception est levée
    with pytest.raises(AssuranceInexistanteError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            date_debut=future_date,
            duree=7,
            assurance_id=999  # ID d'assurance inexistant
        )


def test_vehicule_non_disponible(mock_repositories, future_date):
    """Test de la non-disponibilité du véhicule"""
    # Modifier le mock pour que le véhicule ne soit pas disponible
    mock_repositories['vehicule'].is_available_between.return_value = False
    
    # Vérifier que l'exception est levée
    with pytest.raises(VehiculeNonDisponibleError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            date_debut=future_date,
            duree=7,
            assurance_id=3
        )


def test_date_debut_passee(mock_repositories):
    """Test avec une date de début dans le passé"""
    # Date dans le passé
    past_date = date.today() - timedelta(days=1)
    
    # Vérifier que l'exception est levée
    with pytest.raises(DateInvalideError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            date_debut=past_date,  # Date dans le passé
            duree=7,
            assurance_id=3
        )


def test_duree_negative(mock_repositories, future_date):
    """Test avec une durée négative"""
    # Vérifier que l'exception est levée
    with pytest.raises(DateInvalideError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            date_debut=future_date,
            duree=-7,  # Durée négative
            assurance_id=3
        )


def test_sans_assurance(mock_repositories, future_date):
    """Test sans assurance (paramètre optionnel)"""
    contrat = SignerContratDeLocation.main(
        client_id=1,
        vehicule_id=2,
        date_debut=future_date,
        duree=7,
        assurance_id=None  # Pas d'assurance
    )
    
    # Vérifier que le contrat a été créé correctement
    assert contrat is not None
    assert hasattr(contrat, 'id')
    
    # Vérifier que l'assurance n'a pas été recherchée
    mock_repositories['assurance'].get_by_id.assert_not_called()


def test_erreur_enregistrement_contrat(mock_repositories, future_date):
    """Test de l'échec de l'enregistrement du contrat"""
    # Mock l'échec de l'enregistrement
    mock_repositories['contrat'].save.side_effect = Exception("Erreur de base de données")
    
    # Vérifier que l'exception est levée
    with pytest.raises(ContratLocationError):
        SignerContratDeLocation.main(
            client_id=1,
            vehicule_id=2,
            date_debut=future_date,
            duree=7,
            assurance_id=3
        )


def test_calcul_cout_avec_assurance(mock_repositories, future_date):
    """Test que le coût inclut bien l'assurance"""
    # Configurer les mocks pour les coûts
    vehicule_tarif = 50.0
    assurance_tarif = 10.0
    duree = 7
    vehicule_cout_total = vehicule_tarif * duree
    assurance_cout_total = assurance_tarif * duree
    
    mock_repositories['vehicule'].calculate_rental_cost.return_value = vehicule_cout_total
    mock_repositories['assurance'].get_by_id.return_value = MagicMock(getTarif=lambda: assurance_tarif)
    
    # Exécuter la fonction à tester
    contrat = SignerContratDeLocation.main(
        client_id=1,
        vehicule_id=2,
        date_debut=future_date,
        duree=duree,
        assurance_id=3
    )
    
    # Vérifier que le coût total inclut l'assurance
    assert contrat.getCout() == vehicule_cout_total + assurance_cout_total