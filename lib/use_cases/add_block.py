from lib.domain.Blockchain import Blockchain
from lib.domain.Block import Block
from lib.domain.utils import calculate_merkle_root
from lib.use_cases.get_last_hash import get_last_hash_use_case
from lib.use_cases.get_difficulty import get_difficulty_use_case
from lib.use_cases.change_difficulty import increase_difficulty_use_case
from lib.use_cases.get_height import get_height_use_case
from lib.repository.repository import Repository

from Crypto.Hash import SHA256


def add_block_use_case(blockchain: Blockchain, block: Block, repository: Repository):
    assert SHA256.new(SHA256.new(block.to_blockchain_model()).hexdigest().encode()).hexdigest().startswith("0" * blockchain.difficulty), "Failed in Proof of Work check"
    assert calculate_merkle_root(block.tx) == block.merkle_root, "Failed in Merkle Root check"
    assert block.previous_hash == get_last_hash_use_case(blockchain), "Failed in Previous Hash check"
    assert block.difficulty == get_difficulty_use_case(blockchain), "Failed in difficulty check"
    assert block.height == get_height_use_case(blockchain), "Failed in height check"

    repository.create(block)
    increase_difficulty_use_case(blockchain)
