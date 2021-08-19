import time
from dataclasses import dataclass
from typing import List

from lib.domain.Block import Block
from lib.repository.repository import Repository

@dataclass
class Blockchain:

    chain : List[Block]
    difficulty: int

    def __init__(self, repository: Repository):
        self.chain = []
        self.difficulty = 2

        if len(repository.list()) == 0:
            # Creating genesis block
            genesis_block = Block(
                nounce = 1,
                timestamp = time.time(),
                message = "Bloco Gênesis",
                previous_hash = '0'
            )

            repository.create(genesis_block)