from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import psycopg
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# PostgreSQL connection info
conn_info = (
    "dbname=orders_db_ef5t "
    "user=orders_db_ef5t_user "
    "password=j93zTiEEy3RfrIOuodAhIuzpSowuIuYG "
    "host=dpg-d1f8iq3e5dus73fmrdf0-a.singapore-postgres.render.com "
    "port=5432 sslmode=require"
)

SOFTWARE_CODES = {
    "Architecture Pack": "AP",
    "Construction and BIM": "CB",
    "Animation and VFX": "AF",
    "AutoCAD": "AC",
    "Revit": "RV",
    "3ds Max": "3M",
    "Maya": "MA",
    "Navisworks": "NW",
    "Inventor": "IV",
    "MotionBuilder": "MB",
    "Fusion 360": "F3",
    "Flame": "FL"
}

def validate_captcha(data):
    try:
        num1 = int(data.get('captcha_num1'))
        num2 = int(data.get('captcha_num2'))
        answer = int(data.get('captcha_answer'))
        return answer == (num1 + num2)
    except Exception:
        return False

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200

@app.route("/order", methods=["POST"])
def handle_order():
    try:
        data = request.get_json()

        # ---- CAPTCHA Validation ----
        if not validate_captcha(data):
            return jsonify({"success": False, "error": "Invalid captcha answer."}), 400
        # ---- End CAPTCHA Validation ----

        # Read the French form names
        first_name = data.get("prenom")
        last_name = data.get("nom")
        email = data.get("email")
        phone = data.get("phone")
        software = data.get("logiciel")
        payment_method = data.get("paiment")
        contact_method = data.get("contact_Method")  # Note: your form has 'contact_Method'
        message = data.get("message")
        date_now = datetime.utcnow()

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS commandes (
                        id SERIAL PRIMARY KEY,
                        commande_number TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        phone TEXT,
                        software TEXT,
                        payment_method TEXT,
                        contact_method TEXT,
                        message TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO commandes
                        (commande_number, first_name, last_name, email, phone, software, payment_method, contact_method, message, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    None, first_name, last_name, email, phone, software,
                    payment_method, contact_method, message, date_now
                ))
                inserted_id = cur.fetchone()[0]
                code = SOFTWARE_CODES.get(software, "XX")
                date_part = date_now.strftime("%Y%m%d")
                commande_number = f"{code}-{date_part}-{inserted_id}"

                cur.execute(
                    "UPDATE commandes SET commande_number=%s WHERE id=%s",
                    (commande_number, inserted_id)
                )
                conn.commit()

        response = jsonify({
            "success": True,
            "message": "Order recorded successfully",
            "commande_number": commande_number,
            "date": date_now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "redirect": "/thankyou.html"
        })
        response.status_code = 201
        response.headers['Location'] = '/thankyou.html'
        return response

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/contact", methods=["POST"])
def handle_contact():
    try:
        data = request.get_json()

        # ---- CAPTCHA Validation ----
        if not validate_captcha(data):
            return jsonify({"success": False, "error": "Invalid captcha answer."}), 400
        # ---- End CAPTCHA Validation ----

       first_name = data.get("first_name")
       last_name = data.get("last_name")
       email = data.get("email")
       subject = data.get("subject")
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contacts (
                        id SERIAL PRIMARY KEY,
                        prenom TEXT,
                        nom TEXT,
                        email TEXT,
                        subject TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO contacts (prenom, nom, email, subject)
                    VALUES (%s, %s, %s, %s)
                """, (prenom, nom, email, subject))
                conn.commit()

        return jsonify({"success": True, "message": "Message de contact enregistré avec succès"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/school_quote", methods=["POST"])
def handle_school_quote():
    try:
        data = request.get_json()

        # ---- CAPTCHA Validation ----
        if not validate_captcha(data):
            return jsonify({"success": False, "error": "Invalid captcha answer."}), 400
        # ---- End CAPTCHA Validation ----

        first_name = data.get("prenom")
        last_name = data.get("nom")
        email = data.get("email")
        school = data.get("school")
        tools = data.get("tools")
        seat_count = data.get("seat_count")
        subject = data.get("subject")
        date_now = datetime.utcnow()

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS school_quotes (
                        id SERIAL PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        school TEXT,
                        tools TEXT,
                        seat_count INTEGER,
                        subject TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO school_quotes (first_name, last_name, email, school, tools, seat_count, subject, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, email, school, tools, seat_count, subject, date_now))
                conn.commit()

        return jsonify({"success": True, "message": "School quote request recorded successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
