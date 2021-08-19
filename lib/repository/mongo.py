from typing import List
import pymongo

from lib.domain.Block import Block
from lib.repository.repository import Repository


class MongoRepository(Repository):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://fernando:blockchainsper@cluster0.1gkv8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def list(self) -> List[Block]:
        chain = self.client.Blockchain.blocks.find({}, {'_id': False})
        return [Block.from_dict(i) for i in chain]

    def create(self, block: Block):
        self.client.Blockchain.blocks.insert_one(block.to_dict())
