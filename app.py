from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg

app = Flask(__name__)
CORS(app)

# Connexion à PostgreSQL
conn_info = "dbname=orders_db_ef5t user=orders_db_ef5t_user password=j93zTiEEy3RfrIOuodAhIuzpSowuIuYG host=dpg-d1f8iq3e5dus73fmrdf0-a.singapore-postgres.render.com port=5432 sslmode=require"

@app.route("/order", methods=["POST"])
def handle_order():
    data = request.get_json()

    nom = data.get("nom")
    prenom = data.get("prenom")
    email = data.get("email")
    logiciel = data.get("logiciel")
    paiement = data.get("paiement")

    try:
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS commandes (
                        id SERIAL PRIMARY KEY,
                        nom TEXT,
                        prenom TEXT,
                        email TEXT,
                        logiciel TEXT,
                        paiement TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO commandes (nom, prenom, email, logiciel, paiement)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nom, prenom, email, logiciel, paiement))
                conn.commit()

        return jsonify({"success": True, "message": "Commande enregistrée avec succès"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
