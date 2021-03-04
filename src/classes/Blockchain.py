from Crypto.Hash import SHA256
import time


class Blockchain:

    def __init__(self):
        self.chain = []
        # Creating genesis block
        self.difficulty = 0
        self.create_block(
            nounce=1,
            timestamp=time.time(),
            message="Bloco Gênesis",
            previous_hash='0'
        )

    def create_block(self, nounce, timestamp, message, previous_hash):
        block = {
            'timestamp': float(timestamp),
            'message': message,
            'nounce': nounce,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        self.change_difficulty()
        return block

    def change_difficulty(self):
        self.difficulty += 1

    def reduce_difficulty(self):
        if self.difficulty > 0:
            self.difficulty -= 1

    def get_last_block(self):
        return self.chain[-1]

    def get_last_block_hash(self):
        last_block = self.chain[-1]
        timestamp = last_block["timestamp"]
        message = last_block['message']
        nounce = last_block["nounce"]
        previous_hash = last_block["previous_hash"]

        return SHA256.new(f'{timestamp}|{message}|{nounce}|{previous_hash}'.encode()).hexdigest()

    def proof_of_work(self, block):
        timestamp, message, nounce, previous_hash = block.split("|")
        if SHA256.new(block.encode()).hexdigest().startswith("0"*self.difficulty) and previous_hash == self.get_last_block_hash():
            self.create_block(nounce, timestamp, message, previous_hash)
            return True

        return False

    def chain_valid(self):
        for block_index in range(1, len(self.chain)):
            last_block = self.chain[block_index-1]
            timestamp = last_block["timestamp"]
            message = last_block['message']
            nounce = last_block["nounce"]
            previous_hash = last_block["previous_hash"]

            hashed_last_block = SHA256.new(
                f'{timestamp}|{message}|{nounce}|{previous_hash}'.encode()).hexdigest()

            if self.chain[block_index]['previous_hash'] != hashed_last_block:
                return False

        return True
