from lib.domain.Blockchain import Blockchain
from Crypto.Hash import SHA256


def get_last_hash_use_case(blockchain: Blockchain):
    last_block = blockchain.chain[-1]

    return SHA256.new(last_block.to_blockchain_model()).hexdigest()
