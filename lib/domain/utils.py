from Crypto.Hash import SHA256
from typing import List


def double_sha256(tx: str) -> str:
    return SHA256.new(SHA256.new(tx.encode()).hexdigest().encode()).hexdigest() 

def find_merkle_root(leaf_hash: List[str]) -> str:
    hash = []
    hash2 = []

    if len(leaf_hash) % 2 != 0:
        leaf_hash.extend(leaf_hash[-1:])
    
    for leaf in sorted(leaf_hash):
        hash.append(leaf)
        if len(hash) % 2 == 0:
            hash2.append(double_sha256(hash[0] + hash[1]))
            hash == []

    if len(hash2) == 1: return hash2

    return find_merkle_root(hash2)

def calculate_merkle_root(tx: List[str]):
    leaf_hash = []
    
    for transaction in tx:
        leaf_hash.append(double_sha256(transaction))

    return find_merkle_root(leaf_hash)[0]