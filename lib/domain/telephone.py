import dataclasses

@dataclasses.dataclass(frozen=True)
class Telephone:
    numero: str

    def __str__(self) -> str:
        return self.numero
