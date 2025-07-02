from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import psycopg
from datetime import datetime
import bcrypt
from functools import wraps

app = Flask(__name__)

# --- CORRECT CORS CONFIG FOR YOUR FRONTEND DOMAIN ---
CORS(app, resources={r"/*": {"origins": "https://www.neoedu.xyz"}}, supports_credentials=True)

# --- ENSURE SESSION COOKIE CAN BE SENT CROSS-SITE (REQUIRED FOR FRONTEND-BACKEND ON DIFFERENT DOMAINS) ---
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

app.secret_key = 'your_super_secret_admin_key'  # CHANGE THIS for production!

# --- Admin credentials ---
ADMIN_USER = 'raoufadmin'
ADMIN_PASS_HASH = b'$2b$12$TUdIAG2NUfst3gGYhf9q5O.Lgw28tVYoxEp64xQJZ6Z.HPGdUN/gO'  # bcrypt hash

# --- PostgreSQL connection info ---
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

# --- Admin Auth Decorator ---
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# --- Admin Login Endpoint ---
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == ADMIN_USER and bcrypt.checkpw(password.encode(), ADMIN_PASS_HASH):
        session["is_admin"] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

# --- Admin Logout Endpoint ---
@app.route("/admin_logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return jsonify({"success": True})

# --- Whoami endpoint for session debugging ---
@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify({"is_admin": session.get("is_admin", False)})

# --- Admin Tables Endpoints ---
@app.route("/all_commandes", methods=["GET"])
@admin_required
def all_commandes():
    try:
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, commande_number, first_name, last_name, email, phone, software,
                           payment_method, contact_method, message, referral_code, price, date
                    FROM commandes
                    ORDER BY date DESC
                """)
                commandes = [
                    {
                        "id": row[0],
                        "commande_number": row[1],
                        "first_name": row[2],
                        "last_name": row[3],
                        "email": row[4],
                        "phone": row[5],
                        "software": row[6],
                        "payment_method": row[7],
                        "contact_method": row[8],
                        "message": row[9],
                        "referral_code": row[10],
                        "price": float(row[11]) if row[11] is not None else None,
                        "date": row[12].strftime("%Y-%m-%d %H:%M:%S") if row[12] else ""
                    }
                    for row in cur.fetchall()
                ]
        return jsonify({"commandes": commandes}), 200
    except Exception as e:
        return jsonify({"commandes": [], "error": str(e)}), 500

@app.route("/all_contacts", methods=["GET"])
@admin_required
def all_contacts():
    try:
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, email, subject, date
                    FROM contacts
                    ORDER BY date DESC
                """)
                contacts = [
                    {
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "email": row[3],
                        "subject": row[4],
                        "date": row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else ""
                    }
                    for row in cur.fetchall()
                ]
        return jsonify({"contacts": contacts}), 200
    except Exception as e:
        return jsonify({"contacts": [], "error": str(e)}), 500

@app.route("/all_school_quotes", methods=["GET"])
@admin_required
def all_schools():
    try:
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, email, school, tools, seat_count, subject, date
                    FROM school_quotes
                    ORDER BY date DESC
                """)
                schools = [
                    {
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "email": row[3],
                        "school": row[4],
                        "tools": row[5],
                        "seat_count": row[6],
                        "subject": row[7],
                        "date": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else ""
                    }
                    for row in cur.fetchall()
                ]
        return jsonify({"schools": schools}), 200
    except Exception as e:
        return jsonify({"schools": [], "error": str(e)}), 500

# --- Existing endpoints below (unchanged) ---

@app.route("/validate_referral", methods=["POST"])
def validate_referral():
    try:
        data = request.get_json()
        code = data.get("referral_code")
        if not code:
            return jsonify({"valid": False, "error": "No code provided"}), 400

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM influencers WHERE referral_code = %s", (code,))
                exists = cur.fetchone() is not None

        return jsonify({"valid": exists})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500

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

        first_name = data.get("prenom")
        last_name = data.get("nom")
        email = data.get("email")
        phone = data.get("phone")
        software = data.get("logiciel")
        payment_method = data.get("paiment")
        contact_method = data.get("contact_Method")
        message = data.get("message")
        referral_code = data.get("referral_code")
        price = data.get("price")
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
                        referral_code TEXT,
                        price NUMERIC,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO commandes
                        (commande_number, first_name, last_name, email, phone, software, payment_method, contact_method, message, referral_code, price, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    None, first_name, last_name, email, phone, software,
                    payment_method, contact_method, message, referral_code, price, date_now
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

        if not validate_captcha(data):
            return jsonify({"success": False, "error": "Invalid captcha answer."}), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        subject = data.get("subject")

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contacts (
                        id SERIAL PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        subject TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, subject)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, email, subject))
                conn.commit()

        return jsonify({"success": True, "message": "Message de contact enregistré avec succès"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/school_quote", methods=["POST"])
def handle_school_quote():
    try:
        data = request.get_json()

        if not validate_captcha(data):
            return jsonify({"success": False, "error": "Invalid captcha answer."}), 400

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

@app.route("/login_influencer", methods=["POST"])
def login_influencer():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "error": "Username and password required"}), 400

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS influencers (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        referral_code TEXT,
                        email TEXT
                    )
                """)
                cur.execute("SELECT password_hash, referral_code, email FROM influencers WHERE username=%s", (username,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Invalid username or password"}), 401
                password_hash, referral_code, email = row
                if bcrypt.checkpw(password.encode(), password_hash.encode()):
                    return jsonify({
                        "success": True,
                        "message": "Login successful",
                        "referral_code": referral_code,
                        "email": email
                    }), 200
                else:
                    return jsonify({"success": False, "error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/orders_by_referral", methods=["POST"])
def orders_by_referral():
    try:
        data = request.get_json()
        referral_code = data.get("referral_code")
        if not referral_code:
            return jsonify({"success": False, "error": "Referral code required"}), 400

        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, email, phone, software, payment_method, date, price
                    FROM commandes
                    WHERE referral_code = %s
                    ORDER BY date DESC
                """, (referral_code,))
                orders = [
                    {
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "email": row[3],
                        "phone": row[4],
                        "software": row[5],
                        "payment_method": row[6],
                        "date": row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else "",
                        "price": float(row[8]) if row[8] is not None else None
                    }
                    for row in cur.fetchall()
                ]
        return jsonify({"success": True, "orders": orders}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
