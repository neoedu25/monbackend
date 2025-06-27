from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Configuration PostgreSQL (Render External URL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://orders_db_ef5t_user:j93zTiEEy3RfrIOuodAhIuzpSowuIuYG@dpg-d1f8iq3e5dus73fmrdf0-a.singapore-postgres.render.com/orders_db_ef5t'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Définition du modèle de commande
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_number = db.Column(db.String(50))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(150))
    logiciel = db.Column(db.String(100))
    paiement = db.Column(db.String(100))

# Route d'envoi des commandes
@app.route('/submit', methods=['POST'])
def submit_order():
    try:
        data = request.get_json()

        last_id = db.session.query(db.func.max(Order.id)).scalar() or 0
        numero = f"CMD-{last_id + 1:04d}"

        new_order = Order(
            order_number=numero,
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            email=data.get('email'),
            logiciel=data.get('logiciel'),
            paiement=data.get('paiement')
        )

        db.session.add(new_order)
        db.session.commit()

        return jsonify({'success': True, 'numero': numero})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Point de test GET
@app.route('/')
def index():
    return "API Flask opérationnelle avec PostgreSQL sur Render"

# Lancement local (à ne pas activer sur Render)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
