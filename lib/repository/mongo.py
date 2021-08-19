from typing import List
import pymongo
import os

from lib.domain.Block import Block
from lib.repository.repository import Repository


class MongoRepository(Repository):
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get("MONGO_URL"))

    def list(self) -> List[Block]:
        chain = self.client.Blockchain.blocks.find({}, {'_id': False})
        return [Block.from_dict(i) for i in chain]

    def create(self, block: Block):
        self.client.Blockchain.blocks.insert_one(block.to_dict())
