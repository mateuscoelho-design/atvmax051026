from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/cliente/<int:codigo>')
def cliente(codigo):

    con = sqlite3.connect("clientes.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM clientes
        WHERE codigo = ?
    """, (codigo,))

    registro = cur.fetchone()

    con.close()

    if not registro:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify(dict(registro))


if __name__ == '__main__':
    app.run(port=5001, debug=True)