from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Connexion à la base PostgreSQL avec la variable d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/submit', methods=['POST'])
def submit_order():
    try:
        data = request.get_json()

        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        logiciel = data.get('logiciel')
        paiement = data.get('paiement')

        if not all([nom, prenom, email, logiciel, paiement]):
            return jsonify({'success': False, 'error': 'Champs manquants'}), 400

        conn = connect_db()
        cur = conn.cursor()

        # Crée la table si elle n'existe pas encore
        cur.execute("""
            CREATE TABLE IF NOT EXISTS commandes (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                numero TEXT,
                nom TEXT,
                prenom TEXT,
                email TEXT,
                logiciel TEXT,
                paiement TEXT
            );
        """)

        # Génère un numéro de commande unique
        cur.execute("SELECT COUNT(*) FROM commandes;")
        count = cur.fetchone()[0] + 1
        numero_commande = f"CMD-{count:04d}"

        # Insère les données
        cur.execute("""
            INSERT INTO commandes (numero, nom, prenom, email, logiciel, paiement)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (numero_commande, nom, prenom, email, logiciel, paiement))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'numero': numero_commande})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Backend opérationnel."

if __name__ == '__main__':
    app.run(debug=True)
