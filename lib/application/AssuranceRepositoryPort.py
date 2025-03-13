from typing import Optional, List
from ..domain.assurance import Assurance

class AssuranceRepositoryPort:
    def __init__(self):
        if type(self) == AssuranceRepositoryPort:
            raise Exception("Abstract classes can't be instantiated")

    def get_by_id(self, assurance_id: int) -> Optional[Assurance]:
        pass

    def get_all(self) -> List[Assurance]:
        pass

    def save(self, assurance: Assurance) -> int:
        pass

    def delete(self, assurance_id: int) -> bool:
        pass

    def find_by_name(self, nom: str) -> List[Assurance]:
        pass

    def create_assurance(self, nom: str) -> Assurance:
        pass
