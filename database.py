
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE = INSTANCE_DIR / "brewvote.db"


def get_connection():
    INSTANCE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS coffees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM coffees"
    ).fetchone()[0]

    if count == 0:

        coffees = [
            (
                "Classic Cappuccino",
                "Milk Based",
                "Rich espresso with silky steamed milk and foam.",
                "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800"
            ),
            (
                "Caramel Macchiato",
                "Specialty",
                "Smooth espresso blended with creamy caramel.",
                "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800"
            ),
            (
                "Iced Americano",
                "Cold Coffee",
                "Bold espresso served over refreshing ice.",
                "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=800"
            ),
            (
                "Mocha Delight",
                "Chocolate",
                "A delicious combination of espresso and chocolate.",
                "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=800"
            ),
            (
                "Vanilla Latte",
                "Milk Based",
                "Smooth espresso with vanilla and steamed milk.",
                "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=800"
            ),
            (
                "Cold Brew",
                "Cold Coffee",
                "Slow-steeped coffee with a naturally smooth taste.",
                "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=800"
            )
        ]

        connection.executemany("""
            INSERT INTO coffees
            (name, category, description, image)
            VALUES (?, ?, ?, ?)
        """, coffees)

    connection.commit()
    connection.close()


def get_all_coffees():

    connection = get_connection()

    coffees = connection.execute("""
        SELECT * FROM coffees
        ORDER BY votes DESC, name ASC
    """).fetchall()

    connection.close()

    return coffees


def cast_vote(coffee_id):

    connection = get_connection()

    cursor = connection.execute("""
        UPDATE coffees
        SET votes = votes + 1
        WHERE id = ?
    """, (coffee_id,))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated


def get_statistics():

    connection = get_connection()

    stats = connection.execute("""
        SELECT
            COUNT(*) AS total_coffees,
            COALESCE(SUM(votes), 0) AS total_votes,
            COALESCE(MAX(votes), 0) AS highest_votes
        FROM coffees
    """).fetchone()

    connection.close()

    return stats
