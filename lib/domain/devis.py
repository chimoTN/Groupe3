import dataclasses
import uuid
from datetime import date
from .vehicule import Vehicule

@dataclasses.dataclass
class Devis():
    vehicule: Vehicule
    prix: float
    id: uuid.UUID = uuid.uuid4()
    date = date.today()
