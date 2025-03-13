import dataclasses

@dataclasses.dataclass(frozen=True)
class Email:
    email: str

    def __str__(self) -> str:
        return self.email
