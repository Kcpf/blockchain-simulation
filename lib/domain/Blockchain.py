import time
from dataclasses import dataclass
from typing import List

from lib.domain.Block import Block
from lib.domain.utils import calculate_merkle_root
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
            tx = ["Genesis block"]

            genesis_block = Block(
                previous_hash = '0',
                merkle_root = calculate_merkle_root(tx),
                timestamp = time.time(),
                difficulty = 0,
                nonce = 0,
                height = 0,
                tx=tx
            )

            repository.create(genesis_block)