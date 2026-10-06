from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/compras/<int:cliente>')
def compras(cliente):

    con = psycopg2.connect(
    host="ep-patient-fog-aeynisgn-pooler.c-2.us-east-2.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="npg_br2q6GfJtUpQ",
    port=5432,
    sslmode="require"
)

    cur = con.cursor()

    cur.execute("""
        SELECT
            data_compra,
            valor
        FROM compras
        WHERE codigo_cliente = %s
    """, (cliente,))

    registros = cur.fetchall()

    con.close()

    resultado = []

    for item in registros:
        resultado.append({
            "data": item[0].strftime("%Y-%m-%d"),
            "valor": float(item[1])
        })

    return jsonify(resultado)


if __name__ == '__main__':
    app.run(port=5002, debug=True)