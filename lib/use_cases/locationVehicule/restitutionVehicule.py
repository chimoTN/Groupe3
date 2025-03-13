from lib.repositories.clientRepository import ClientRepository
from lib.repositories.vehiculeRepository import VehiculeRepository

def RestitutionVehicule(client_id: int, vehicule_id: int, km_parcourus: int, etat: str = "Propre"):
    
    client_repo = ClientRepository()
    vehicule_repo = VehiculeRepository()
    
    client = client_repo.get_by_id(client_id)
    vehicule = vehicule_repo.get_by_id(vehicule_id)
    
    if not client:
        print("Client non trouvé.")
        return
    
    if not vehicule:
        print("Véhicule non trouvé.")
        return
    
    if vehicule not in client.historique_locations:
        print(f"Le client {client.nom} {client.prenom} n'a pas loué cette voiture.")
        return
    
    # Gestion des cas spécifiques
    if etat.lower() == "sale":
        print(f"Le client {client.nom} {client.prenom} a rendu la voiture {vehicule.marque} {vehicule.modele} en mauvais état (Sale). Des frais de nettoyage peuvent être appliqués.")
    elif etat.lower() == "cassé":
        print(f"Le client {client.nom} {client.prenom} a rendu la voiture {vehicule.marque} {vehicule.modele} endommagée. Des frais de réparation seront facturés.")
    elif etat.lower() == "non rendu":
        print(f"Le client {client.nom} {client.prenom} n'a pas retourné la voiture {vehicule.marque} {vehicule.modele}. Des pénalités peuvent être appliquées.")
        return
    else:
        print(f"Le client {client.nom} {client.prenom} a retourné la voiture {vehicule.marque} {vehicule.modele} en bon état.")
    
    # Met à jour les informations du véhicule et du client
    vehicule.retourner(km_parcourus, etat)
    client.historique_locations.remove(vehicule)
    print(f"Mise à jour effectuée pour le véhicule {vehicule.marque} {vehicule.modele}.")

# Exemple d'utilisation
def test_use_case():
    client_repo = ClientRepository()
    vehicule_repo = VehiculeRepository()
    
    client = client_repo.create_client("Dupont", "Jean", "123456", "0600000000", "jean.dupont@example.com")
    vehicule = vehicule_repo.create_vehicule("Peugeot", "208", 2021, "AB-123-CD", 25000, 45.0, "Bon", "Voiture")
    
    client.louer_voiture(vehicule)
    
    print("\n--- Cas normal ---")
    RestitutionVehicule(client.id, vehicule.id, 300, "Propre")
    
    print("\n--- Cas voiture sale ---")
    RestitutionVehicule(client.id, vehicule.id, 300, "Sale")
    
    print("\n--- Cas voiture cassée ---")
    RestitutionVehicule(client.id, vehicule.id, 300, "Cassé")
    
    print("\n--- Cas voiture non retournée ---")
    RestitutionVehicule(client.id, vehicule.id, 0, "Non Rendu")
    
# Lancer les tests
test_use_case()
