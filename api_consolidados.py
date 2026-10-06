from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Mantenha aqui a mesma conexão que já está funcionando no seu arquivo
MONGODB_URI = "mongodb+srv://mateuscoelho_db_user:mateus0806@aulamax21092026.2xkgyzi.mongodb.net/"

mongo = MongoClient(MONGODB_URI)

db = mongo["integracao_dados"]
colecao = db["cliente_consolidado"]


# CONSULTA DOS DADOS CONSOLIDADOS
@app.route('/consolidados')
def consolidados():

    lista = []

    for doc in colecao.find():
        doc["_id"] = str(doc["_id"])
        lista.append(doc)

    return jsonify(lista)


# RANKING DOS CLIENTES POR VOLUME DE COMPRAS
@app.route('/ranking-clientes')
def ranking_clientes():

    pipeline = [
        {
            "$unwind": "$compras"
        },
        {
            "$group": {
                "_id": "$cliente.nome",
                "total_compras": {
                    "$sum": "$compras.valor"
                }
            }
        },
        {
            "$sort": {
                "total_compras": -1
            }
        },
        {
            "$project": {
                "_id": 0,
                "cliente": "$_id",
                "total_compras": 1
            }
        }
    ]

    resultado = list(
        colecao.aggregate(pipeline)
    )

    return jsonify(resultado)


if __name__ == '__main__':
    app.run(port=5005, debug=True)