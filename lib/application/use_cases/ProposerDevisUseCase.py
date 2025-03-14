import dataclasses
from ...domain.vehicule import Vehicule
from ...domain.devis import Devis
from ..exceptions import VehiculeIntrouvableException, PrixDevisInvalideException
from ...infrastructure.InMemoryDevisRepository import InMemoryDevisRepository
from ...infrastructure.InMemoryVehiculeRepository import InMemoryVehiculeRepository

@dataclasses.dataclass
class ProposerDevisUseCase:
    vehiculeRepository: InMemoryVehiculeRepository = InMemoryVehiculeRepository()
    devisRepository: InMemoryDevisRepository = InMemoryDevisRepository()

    def proposerDevis(self, vehicule: Vehicule, prix: int) -> Devis:
        if vehicule is None:
            raise VehiculeIntrouvableException("Vehicule invalide")

        if prix < 0:
            raise PrixDevisInvalideException()
        
        known_vehicule = self.vehiculeRepository.get_by_immatriculation(vehicule.immatriculation)
        if known_vehicule is None:
            self.vehiculeRepository.save(vehicule)

        self.devisRepository.save(Devis(vehicule, prix))
        
        devis = Devis(vehicule, prix)
        return devis
