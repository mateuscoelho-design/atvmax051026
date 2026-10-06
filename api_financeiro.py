from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://integracao-dados-ce400-default-rtdb.firebaseio.com/"
    }
)

app = Flask(__name__)

@app.route('/financeiro/<codigo>')
def financeiro(codigo):

    ref = db.reference("/")
    dados = ref.child(codigo).get()

    if not dados:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify(dados)

if __name__ == '__main__':
    app.run(port=5003, debug=True)