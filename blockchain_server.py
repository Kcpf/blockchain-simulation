from Crypto.Hash import SHA256
import json
import flask
import os
import threading
import time
from flask import Flask, jsonify


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


app = Flask(__name__)


blockchain = Blockchain()


@app.route('/blocks', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/blocks/last_hash', methods=['GET'])
def display_last_hash():
    response = {'last_hash': blockchain.get_last_block_hash()}
    return jsonify(response), 200


@app.route('/blocks/difficulty', methods=['GET'])
def display_difficulty():
    response = {'difficulty': blockchain.difficulty}
    return jsonify(response), 200


@app.route('/blocks/mine', methods=['POST'])
def mine():
    block = flask.request.json["block"]
    if block == None:
        return "Invalid POST", 500

    result = blockchain.proof_of_work(block)
    if result:
        return jsonify(blockchain.get_last_block()), 200
    else:
        return "Algo deu errado, tente novamente!", 500


@app.route('/blocks/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid()

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


def difficulty():
    while True:
        blockchain.reduce_difficulty()
        time.sleep(3600)


if __name__ == "__main__":
    x = threading.Thread(target=difficulty, daemon=True)
    x.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
