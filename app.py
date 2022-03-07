import json
import flask
import os
import time
import threading
from flask import Flask, jsonify

from lib.domain.Blockchain import Blockchain
from lib.domain.Block import Block
from lib.use_cases.get_chain import get_chain_use_case
from lib.use_cases.add_block import add_block_use_case
from lib.use_cases.check_validity import check_validity_use_case
from lib.use_cases.get_difficulty import get_difficulty_use_case
from lib.use_cases.get_last_hash import get_last_hash_use_case
from lib.use_cases.change_difficulty import reduce_difficulty_use_case
from lib.use_cases.get_height import get_height_use_case
from lib.repository.memory import MemoryRepository
from lib.repository.mongo import MongoRepository

app = Flask(__name__)

repository = MongoRepository()
blockchain = Blockchain(repository)

@app.before_request
def update_chain():
    blockchain.chain = repository.list()

@app.route('/', methods=['GET'])
def display_chain():
    chain = get_chain_use_case(blockchain)
    response = {"chain": chain, "length": len(chain)}

    return jsonify(response), 200

@app.route('/info', methods=['GET'])
def display_info():
    valid = check_validity_use_case(blockchain)
    last_hash = get_last_hash_use_case(blockchain)
    difficulty = get_difficulty_use_case(blockchain)
    height = get_height_use_case(blockchain)

    response = {
        "valid": valid,
        "last_hash": last_hash,
        "difficulty": difficulty,
        "height": height
    }

    return jsonify(response), 200

@app.route('/mine', methods=['POST'])
def mine():
    block_information = flask.request.get_json()

    block = Block(
        block_information["height"],
        block_information["previous_hash"],
        block_information["merkle_root"],
        block_information["timestamp"],
        block_information["difficulty"],
        block_information["nonce"],
        block_information["tx"],
    )

    try:
        add_block_use_case(blockchain, block, repository)
    except AssertionError as error:
        return f"Algo deu errado, tente novamente!\n{error}", 500

    return "Bloco foi minerado com sucesso", 200

def difficulty():
    while True:
        reduce_difficulty_use_case(blockchain)
        time.sleep(300)


if __name__ == "__main__":
    x = threading.Thread(target=difficulty, daemon=True)
    x.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # Local
    # app.run(host='127.0.0.1', port=port)
