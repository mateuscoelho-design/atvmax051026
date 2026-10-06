from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

MONGODB_URI = "mongodb+srv://mateuscoelho_db_user:mateus0806@aulamax21092026.2xkgyzi.mongodb.net/"

mongo = MongoClient(MONGODB_URI)

db = mongo["integracao_dados"]
colecao = db["cliente_consolidado"]


@app.route('/exportar')
def exportar():

    registros = []

    for doc in colecao.find():

        registros.append({
            "codigo":
                doc["cliente"]["codigo"],

            "nome":
                doc["cliente"]["nome"],

            "cidade":
                doc["cliente"]["cidade"],

            "limite":
                doc["financeiro"]["limite"],

            "saldo":
                doc["financeiro"]["saldo"]
        })

    df = pd.DataFrame(registros)

    df.to_excel(
        "clientes_consolidados.xlsx",
        index=False
    )

    return jsonify({
        "arquivo":
        "clientes_consolidados.xlsx"
    })


if __name__ == '__main__':
    app.run(port=5006, debug=True)