import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "products.db"


def main() -> None:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products")
    cursor.executemany(
        "INSERT INTO products (title, price, count) VALUES (?, ?, ?)",
        [
            ("Keyboard", 2490.0, 6),
            ("Mouse", 1390.0, 9),
        ],
    )

    connection.commit()
    connection.close()
    print("Initial products inserted successfully.")


if __name__ == "__main__":
    main()
