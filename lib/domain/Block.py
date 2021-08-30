import dataclasses
import sys
from typing import List


@dataclasses.dataclass
class Block:
    height: int
    previous_hash: str
    merkle_root: str
    timestamp: float
    difficulty: int
    nonce: int
    tx: List[str]

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)

    def to_blockchain_model(self):
        return f'{self.height}{self.previous_hash}{self.merkle_root}{self.timestamp}{self.difficulty}{self.nonce}'.encode()
