import json
import flask
import os
import time
import threading
from flask import Flask, jsonify
from flask import render_template

from classes.Blockchain import Blockchain

app = Flask(__name__)


blockchain = Blockchain()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
    # Local
    # app.run(host='127.0.0.1', port=port)
