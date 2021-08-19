from lib.domain.Blockchain import Blockchain


def increase_difficulty_use_case(blockchain: Blockchain):
    blockchain.difficulty += 1


def reduce_difficulty_use_case(blockchain: Blockchain):
    if blockchain.difficulty > 2:
        blockchain.difficulty -= 1