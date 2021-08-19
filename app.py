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
from lib.repository.memory import MemoryRepository
from lib.repository.mongo import MongoRepository

app = Flask(__name__)

repository = MongoRepository()
blockchain = Blockchain(repository)

@app.before_request
def update_chain():
    blockchain.chain = repository.list()


@app.route('/blocks', methods=['GET'])
def display_chain():
    chain = get_chain_use_case(blockchain)
    response = {"chain": chain, "length": len(chain)}

    return jsonify(response), 200


@app.route('/blocks/last_hash', methods=['GET'])
def display_last_hash():
    response = {"last_hash": get_last_hash_use_case(blockchain)}

    return jsonify(response), 200


@app.route('/blocks/difficulty', methods=['GET'])
def display_difficulty():
    response = {"difficulty": get_difficulty_use_case(blockchain)} 

    return jsonify(response), 200


@app.route('/blocks/mine', methods=['POST'])
def mine():
    block_information = flask.request.json["block"]
    
    if block_information == None: return "Invalid POST", 500

    timestamp, message, nounce, previous_hash = block_information.split("|")

    block = Block(
        nounce,
        timestamp,
        message,
        previous_hash
    )

    result = add_block_use_case(blockchain, block, repository)

    if result: return "Bloco foi minerado com sucesso", 200
    
    return "Algo deu errado, tente novamente!", 500


@app.route('/blocks/valid', methods=['GET'])
def valid():
    valid = check_validity_use_case(blockchain)

    if valid:
        response = {'message': 'Blockchain é válida.'}
    else:
        response = {'message': 'Blockchain não é válida.'}
        
    return jsonify(response), 200


def difficulty():
    while True:
        reduce_difficulty_use_case(blockchain)
        time.sleep(3600)


if __name__ == "__main__":
    x = threading.Thread(target=difficulty, daemon=True)
    x.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # Local
    # app.run(host='127.0.0.1', port=port)
