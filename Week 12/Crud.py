import sqlite3

DB_NAME = 'app.db'  # single place to change the DB path

def create_database():
    """Creates the database and users table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    create_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL,
            age  INTEGER NOT NULL
        )
    '''
    cursor.execute(create_table)
    conn.commit()
    conn.close()


def add_user(name: str, age: int):
    """Inserts a new user into the users table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    insert = 'INSERT INTO users (name, age) VALUES (?, ?)'
    cursor.execute(insert, (name, age))

    conn.commit()
    conn.close()


# --- usage ---
if __name__ == '__main__':
    create_database()
    add_user("Ali", 23)
    add_user("Sara", 19)













