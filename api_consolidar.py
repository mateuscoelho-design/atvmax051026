from flask import Flask, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

MONGODB_URI = "mongodb+srv://mateuscoelho_db_user:mateus0806@aulamax21092026.2xkgyzi.mongodb.net/"

mongo = MongoClient(MONGODB_URI)

db = mongo["integracao_dados"]
colecao = db["cliente_consolidado"]


@app.route('/consolidar/<codigo>')
def consolidar(codigo):

    cliente = requests.get(
        f'http://localhost:5001/cliente/{codigo}'
    ).json()

    compras = requests.get(
        f'http://localhost:5002/compras/{codigo}'
    ).json()

    financeiro = requests.get(
        f'http://localhost:5003/financeiro/{codigo}'
    ).json()

    documento = {
        "cliente": cliente,
        "compras": compras,
        "financeiro": financeiro
    }

    colecao.insert_one(documento)

    return jsonify({
        "status": "sucesso",
        "cliente": codigo
    })


if __name__ == '__main__':
    app.run(port=5004, debug=True)