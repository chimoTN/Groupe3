from flask import Blueprint, request, jsonify
from lib.application.VehiculeRepositoryPort import VehiculeRepositoryPort
from lib.domain.vehicule import Vehicule
from datetime import date

from lib.infrastructure.InMemoryVehiculeRepository import InMemoryVehiculeRepository

vehicule_bp = Blueprint('vehicule_bp', __name__)

class VehiculeController:
    def __init__(self, repository: VehiculeRepositoryPort):
        self.repository = repository

    @vehicule_bp.route('/vehicules/<int:vehicule_id>', methods=['GET'])
    def get_vehicule(vehicule_id):
        vehicule = vehicule_controller.repository.get_by_id(vehicule_id)
        if vehicule:
            return jsonify(vehicule.to_dict()), 200
        return jsonify({'error': 'Vehicule not found'}), 404

    @vehicule_bp.route('/vehicules', methods=['GET'])
    def get_all_vehicules():
        vehicules = vehicule_controller.repository.get_all()
        return jsonify([vehicule.to_dict() for vehicule in vehicules]), 200

    @vehicule_bp.route('/vehicules/available', methods=['GET'])
    def get_available_vehicules():
        vehicules = vehicule_controller.repository.get_available()
        return jsonify([vehicule.to_dict() for vehicule in vehicules]), 200

    @vehicule_bp.route('/vehicules', methods=['POST'])
    def create_vehicule():
        data = request.json
        vehicule = vehicule_controller.repository.create_vehicule(
            marque=data['marque'],
            modele=data['modele'],
            annee=data['annee'],
            immatriculation=data['immatriculation'],
            kilometrage=data['kilometrage'],
            prix_journalier=data['prix_journalier'],
            etat=data['etat'],
            type_vehicule=data['type_vehicule']
        )
        return jsonify(vehicule.to_dict()), 201

    @vehicule_bp.route('/vehicules/<int:vehicule_id>', methods=['DELETE'])
    def delete_vehicule(vehicule_id):
        success = vehicule_controller.repository.delete(vehicule_id)
        if success:
            return jsonify({'message': 'Vehicule deleted'}), 200
        return jsonify({'error': 'Vehicule not found'}), 404

    @vehicule_bp.route('/vehicules/<int:vehicule_id>/availability', methods=['PATCH'])
    def set_availability(vehicule_id):
        data = request.json
        success = vehicule_controller.repository.set_availability(vehicule_id, data['disponible'])
        if success:
            return jsonify({'message': 'Availability updated'}), 200
        return jsonify({'error': 'Vehicule not found'}), 404

    @vehicule_bp.route('/vehicules/<int:vehicule_id>/rent', methods=['POST'])
    def louer_vehicule(vehicule_id):
        success = vehicule_controller.repository.louer_vehicule(vehicule_id)
        if success:
            return jsonify({'message': 'Vehicule rented'}), 200
        return jsonify({'error': 'Vehicule not available'}), 404

    @vehicule_bp.route('/vehicules/<int:vehicule_id>/return', methods=['POST'])
    def retourner_vehicule(vehicule_id):
        data = request.json
        success = vehicule_controller.repository.retourner_vehicule(vehicule_id, data['km_parcourus'])
        if success:
            return jsonify({'message': 'Vehicule returned'}), 200
        return jsonify({'error': 'Vehicule not found'}), 404

    @vehicule_bp.route('/vehicules/<int:vehicule_id>/rental_cost', methods=['GET'])
    def calculate_rental_cost(vehicule_id):
        duree = int(request.args.get('duree'))
        cost = vehicule_controller.repository.calculate_rental_cost(vehicule_id, duree)
        return jsonify({'rental_cost': cost}), 200

    @vehicule_bp.route('/vehicules/search', methods=['GET'])
    def find_by_criteria():
        criteria = {
            'marque': request.args.get('marque'),
            'modele': request.args.get('modele'),
            'disponible': request.args.get('disponible'),
            'type_vehicule': request.args.get('type_vehicule'),
            'prix_max': request.args.get('prix_max')
        }
        vehicules = vehicule_controller.repository.find_by_criteria(**criteria)
        return jsonify([vehicule.to_dict() for vehicule in vehicules]), 200


repository = InMemoryVehiculeRepository()
vehicule_controller = VehiculeController(repository)