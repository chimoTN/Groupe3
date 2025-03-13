import dataclasses
from datetime import date

@dataclasses.dataclass()
class Permis:
    numero: str
    categorie: list[str]
    date_delivrance: date
    date_expiration: date
    detenteur: str

    def __str__(self) -> str:
        return self.numero + " " + self.detenteur