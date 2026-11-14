
from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = "coffee.db"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS coffees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image TEXT,
            votes INTEGER DEFAULT 0
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM coffees"
    ).fetchone()[0]

    if count == 0:
        coffees = [
            (1, "Espresso", "Hot Coffee",
             "Strong and rich classic espresso.",
             "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=800", 0),

            (2, "Cappuccino", "Hot Coffee",
             "Espresso with steamed milk and foam.",
             "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800", 0),

            (3, "Latte", "Hot Coffee",
             "Smooth coffee with creamy milk.",
             "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800", 0),

            (4, "Mocha", "Hot Coffee",
             "Chocolate blended with espresso and milk.",
             "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=800", 0),

            (5, "Iced Coffee", "Cold Coffee",
             "Refreshing chilled coffee.",
             "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800", 0),

            (6, "Cold Brew", "Cold Coffee",
             "Slow-steeped coffee with a smooth taste.",
             "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=800", 0)
        ]

        conn.executemany("""
            INSERT INTO coffees
            (id, name, category, description, image, votes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, coffees)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    conn = get_db_connection()
    coffees = conn.execute(
        "SELECT * FROM coffees ORDER BY votes DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", coffees=coffees)


# Vote for coffee
@app.route("/vote/<int:coffee_id>", methods=["POST"])
def vote(coffee_id):
    conn = get_db_connection()

    coffee = conn.execute(
        "SELECT * FROM coffees WHERE id = ?",
        (coffee_id,)
    ).fetchone()

    if coffee is None:
        conn.close()
        return jsonify({"success": False, "message": "Coffee not found"}), 404

    conn.execute(
        "UPDATE coffees SET votes = votes + 1 WHERE id = ?",
        (coffee_id,)
    )

    updated = conn.execute(
        "SELECT votes FROM coffees WHERE id = ?",
        (coffee_id,)
    ).fetchone()

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "votes": updated["votes"]
    })


# Leaderboard
@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    coffees = conn.execute(
        "SELECT * FROM coffees ORDER BY votes DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(coffee) for coffee in coffees])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
