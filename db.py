import sqlite3
from contextlib import contextmanager

@contextmanager
def db_connection():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()

def create_table():
    with db_connection() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS matches
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           player1 TEXT,
                           player2 TEXT,
                           winner TEXT,
                           timestamp TIMESTAMP DEFAULT 0)''')

def save_match_result(player1, player2, winner, timestamp):
    with db_connection() as cursor:
        cursor.execute('''INSERT INTO matches (player1, player2, winner, timestamp) VALUES (?, ?, ?, ?)''', (player1, player2, winner, timestamp))
        
def close_db_connection():
    with db_connection() as cursor:
        cursor.close()

def get_result():
    with db_connection() as cursor:
        cursor.execute("SELECT * FROM matches")
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        res = []
        for row in results:
            res.append(dict(zip(columns, row)))
    return res