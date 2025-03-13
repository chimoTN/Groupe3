from typing import Optional, List
import dataclasses
import abc
from ..domain.assurance import Assurance


class AssuranceRepositoryPort(abc.ABC):
    @abc.abstractmethod
    # def __init__(self):
        # if type(self) == AssuranceRepositoryPort:
            # raise Exception("Abstract classes can't be instantiated")

    @abc.abstractmethod
    def get_by_id(self, assurance_id: int) -> Optional[Assurance]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Assurance]:
        pass

    @abc.abstractmethod
    def save(self, assurance: Assurance) -> int:
        pass

    @abc.abstractmethod
    def delete(self, assurance_id: int) -> bool:
        pass

    @abc.abstractmethod
    def find_by_name(self, nom: str) -> List[Assurance]:
        pass

    @abc.abstractmethod
    def create_assurance(self, nom: str) -> Assurance:
        pass
