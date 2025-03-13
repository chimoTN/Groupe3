import dataclasses

@dataclasses.dataclass(frozen=True)
class Immatriculation:
    identifiant: str
    departement: str

    def __str__(self) -> str:
        return self.identifiant + " " + self.departement
