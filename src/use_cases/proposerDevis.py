from ..entities.vehicule import Vehicule
from ..entities.devis import Devis

class InvalidDevisPriceException(Exception):
    pass

class ProposerDevisUseCase():
    def __init__(self):
        pass

    def ProposerDevis(vehicule: Vehicule, prix: int) -> Devis:
        if vehicule is None:
            raise Exception("Vehicule invalide")

        if prix < 0:
            raise InvalidDevisPriceException()
        
        devis = Devis(vehicule, prix)
        return devis