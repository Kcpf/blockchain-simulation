from lib.domain.Blockchain import Blockchain

def get_height_use_case(blockchain: Blockchain):
    return len(blockchain.chain) + 1
