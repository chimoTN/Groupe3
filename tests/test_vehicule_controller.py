import pytest
from flask import Flask, jsonify
from lib.application.controllers.VehiculeController import vehicule_bp, VehiculeController
from lib.infrastructure.InMemoryVehiculeRepository import InMemoryVehiculeRepository

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    repository = InMemoryVehiculeRepository()
    vehicule_controller = VehiculeController(repository)
    app.register_blueprint(vehicule_bp, url_prefix='/api')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_vehicule(client):
    response = client.post('/api/vehicules', json={
        "marque": "Toyota",
        "modele": "Corolla",
        "annee": 2020,
        "immatriculation": "ABC123",
        "kilometrage": 15000,
        "prix_journalier": 50.0,
        "etat": "Bon",
        "type_vehicule": "Berline"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['marque'] == "Toyota"
    assert data['modele'] == "Corolla"

def test_get_all_vehicules(client):
    client.post('/api/vehicules', json={
        "marque": "Toyota",
        "modele": "Corolla",
        "annee": 2020,
        "immatriculation": "ABC123",
        "kilometrage": 15000,
        "prix_journalier": 50.0,
        "etat": "Bon",
        "type_vehicule": "Berline"
    })
    response = client.get('/api/vehicules')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_get_vehicule(client):
    client.post('/api/vehicules', json={
        "marque": "Toyota",
        "modele": "Corolla",
        "annee": 2020,
        "immatriculation": "ABC123",
        "kilometrage": 15000,
        "prix_journalier": 50.0,
        "etat": "Bon",
        "type_vehicule": "Berline"
    })
    response = client.get('/api/vehicules/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['marque'] == "Toyota"
    assert data['modele'] == "Corolla"

def test_delete_vehicule(client):
    client.post('/api/vehicules', json={
        "marque": "Toyota",
        "modele": "Corolla",
        "annee": 2020,
        "immatriculation": "ABC123",
        "kilometrage": 15000,
        "prix_journalier": 50.0,
        "etat": "Bon",
        "type_vehicule": "Berline"
    })
    response = client.delete('/api/vehicules/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Vehicule deleted'

def test_find_by_criteria(client):
    client.post('/api/vehicules', json={
        "marque": "Toyota",
        "modele": "Corolla",
        "annee": 2020,
        "immatriculation": "ABC123",
        "kilometrage": 15000,
        "prix_journalier": 50.0,
        "etat": "Bon",
        "type_vehicule": "Berline"
    })
    response = client.get('/api/vehicules/search?marque=Toyota&modele=Corolla')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['marque'] == "Toyota"
    assert data[0]['modele'] == "Corolla"