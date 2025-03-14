import abc
import dataclasses
from typing import Optional, List

from ..domain.devis import Devis
from ..domain.immatriculation import Immatriculation

class DevisRepositoryPort(abc.ABC):
    @abc.abstractmethod
    def get_by_immatriculation(self, immatriculation: Immatriculation) -> list[Devis]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Devis]:
        pass

    @abc.abstractmethod
    def save(self, devis: Devis):
        pass

    @abc.abstractmethod
    def delete(self, devis: Devis):
        pass

    @abc.abstractmethod
    def clear(self):
        pass


