from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


# ---------------- DATABASE ---------------- #
def get_db():
    conn = sqlite3.connect("taxi.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # User table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Feedback table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()


init_db()

@app.route('/')
def home():
    return render_template('index.html')
# ---------------- REGISTER ---------------- #
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email, mobile, password) VALUES (?, ?, ?, ?)",
            (data['name'], data['email'], data['mobile'], data['password'])
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except sqlite3.IntegrityError:
        return jsonify({"error": "Mobile already exists"}), 400


# ---------------- LOGIN ---------------- #
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE mobile=? AND password=?",
        (data['mobile'], data['password'])
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login success",
            "user": dict(user)
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ---------------- PROFILE ---------------- #
@app.route('/profile/<mobile>', methods=['GET'])
def profile(mobile):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name, email, mobile FROM users WHERE mobile=?", (mobile,))
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "User not found"}), 404


# ---------------- FEEDBACK ---------------- #
@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO feedback (name, rating, message) VALUES (?, ?, ?)",
        (data['name'], data['rating'], data['message'])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback added"})


@app.route('/feedback', methods=['GET'])
def get_feedback():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM feedback")
    rows = cur.fetchall()
    conn.close()

    feedback_list = [dict(row) for row in rows]

    return jsonify(feedback_list)


# ---------------- RUN ---------------- #
if __name__ == '__main__':
    app.run(debug=True)
