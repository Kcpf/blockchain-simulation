import dataclasses


@dataclasses.dataclass
class Block:
    nounce: int
    timestamp: float
    message: str
    previous_hash: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)

    def to_blockchain_model(self):
        return f'{self.timestamp}|{self.message}|{self.nounce}|{self.previous_hash}'.encode()
