import dataclasses
from .vehicule import Vehicule

@dataclasses.dataclass
class Devis():
    vehicule: Vehicule
    prix: float
