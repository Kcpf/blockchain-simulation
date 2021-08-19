from lib.domain.Blockchain import Blockchain

def get_chain_use_case(blockchain: Blockchain):
    chain = [block.to_dict() for block in blockchain.chain]

    return chain    