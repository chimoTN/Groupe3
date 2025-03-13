from ...domain.vehicule import Vehicule
from ...domain.devis import Devis
from ..exceptions import VehiculeIntrouvableException, PrixDevisInvalideException

class ProposerDevisUseCase:
    def proposerDevis(self, vehicule: Vehicule, prix: int) -> Devis:
        if vehicule is None:
            raise VehiculeIntrouvableException("Vehicule invalide")

        if prix < 0:
            raise PrixDevisInvalideException()

        devis = Devis(vehicule, prix)
        return devis
