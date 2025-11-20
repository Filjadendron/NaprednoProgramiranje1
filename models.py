import sqlite3

def init_db():
    conn = sqlite3.connect('troskovi.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Lokacije (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naziv TEXT UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Troskovi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naziv TEXT NOT NULL,
            iznos REAL NOT NULL,
            tip TEXT NOT NULL,
            namena TEXT NOT NULL,
            lokacija_id INTEGER,
            FOREIGN KEY(lokacija_id) REFERENCES Lokacije(id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
