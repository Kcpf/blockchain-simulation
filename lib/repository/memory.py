from typing import List

from lib.domain.Block import Block
from lib.repository.repository import Repository


class MemoryRepository(Repository):
    def __init__(self, data):
        self.data = data
    
    def list(self) -> List[Block]:
        return [Block.from_dict(i) for i in self.data]

    def create(self, block: Block):
        self.data.append(block.to_dict())
