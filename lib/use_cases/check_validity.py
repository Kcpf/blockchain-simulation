from lib.domain.Blockchain import Blockchain
from Crypto.Hash import SHA256


def check_validity_use_case(blockchain: Blockchain):
    for block_index in range(1, len(blockchain.chain)):
        last_block = blockchain.chain[block_index - 1]

        last_block_hash = SHA256.new(last_block.to_blockchain_model()).hexdigest()

        if blockchain.chain[block_index].previous_hash != last_block_hash: return False

    return True
