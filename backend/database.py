import sqlite3

DB_NAME = 'trading.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            action TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_trade(symbol, action, confidence):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO trades (symbol, action, confidence) VALUES (?, ?, ?)', (symbol, action, confidence))
    conn.commit()
    conn.close()

def get_trades():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM trades ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return [
        {'id': row[0], 'symbol': row[1], 'action': row[2], 'confidence': row[3], 'timestamp': row[4]}
        for row in rows
    ]
