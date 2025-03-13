from .vehicule import Vehicule

class Devis():
    vehicule: Vehicule
    prix: int

    def __init__(self, vehicule: Vehicule, prix: int):
        self.vehicule = vehicule
        self.prix = prix
