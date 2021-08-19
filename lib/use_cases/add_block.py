from lib.domain.Blockchain import Blockchain
from lib.domain.Block import Block
from lib.use_cases.get_last_hash import get_last_hash_use_case
from lib.use_cases.change_difficulty import increase_difficulty_use_case
from lib.repository.repository import Repository

from Crypto.Hash import SHA256


def add_block_use_case(blockchain: Blockchain, block: Block, repository: Repository):
    proof_of_work_check = SHA256.new(block.to_blockchain_model()).hexdigest().startswith("0" * blockchain.difficulty)
    previous_block_check = block.previous_hash == get_last_hash_use_case(blockchain)

    if proof_of_work_check and previous_block_check:
        repository.create(block)
        increase_difficulty_use_case(blockchain)
        return True

    return False
