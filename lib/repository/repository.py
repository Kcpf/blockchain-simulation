from abc import ABC, abstractmethod
from typing import List

from lib.domain.Block import Block


class Repository(ABC):
    
    @abstractmethod
    def list(self) -> List[Block]:
        pass

    @abstractmethod
    def create(self, block: Block) -> None:
        pass
