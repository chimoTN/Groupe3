import pytest

from ...domain.devis import Devis
from ..exceptions import DevisIntrouvable


class TerminerPrestationUseCase:
    def terminerPrestation(self, devis: Devis) -> Devis:
        if devis is None:
            raise DevisIntrouvable("Devis invalide")
        
        # TODO: terminer prestation
