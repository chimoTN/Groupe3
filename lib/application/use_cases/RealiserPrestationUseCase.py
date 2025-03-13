import pytest

from ...domain.devis import Devis
from ..exceptions import DevisIntrouvable

class RealiserPrestationUseCase:
    def realiserPrestation(self, devis: Devis) -> Devis:
        if devis is None:
            raise DevisIntrouvable("Devis invalide")
        
        # TODO: realiser prestation
