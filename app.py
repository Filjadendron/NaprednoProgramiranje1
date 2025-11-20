from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB = 'troskovi.db'

def get_db():
    return sqlite3.connect(DB)

@app.route('/troskovi', methods=['GET'])
def get_troskovi():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT Troskovi.id, Troskovi.naziv, Troskovi.iznos, Troskovi.tip, Troskovi.namena, Lokacije.naziv as lokacija 
                 FROM Troskovi LEFT JOIN Lokacije ON Troskovi.lokacija_id = Lokacije.id''')
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/troskovi', methods=['POST'])
def add_trosak():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    # Ensure lokacija exists
    c.execute("INSERT OR IGNORE INTO Lokacije(naziv) VALUES (?)", (data['lokacija'],))
    c.execute("SELECT id FROM Lokacije WHERE naziv=?", (data['lokacija'],))
    lokacija_id = c.fetchone()[0]
    c.execute('''INSERT INTO Troskovi(naziv, iznos, tip, namena, lokacija_id)
                VALUES (?, ?, ?, ?, ?)''', (data['naziv'], float(data['iznos']), data['tip'], data['namena'], lokacija_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/troskovi/<int:id>', methods=['DELETE'])
def delete_trosak(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM Troskovi WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/troskovi/<int:id>', methods=['PUT'])
def update_trosak(id):
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO Lokacije(naziv) VALUES (?)", (data['lokacija'],))
    c.execute("SELECT id FROM Lokacije WHERE naziv=?", (data['lokacija'],))
    lokacija_id = c.fetchone()[0]
    c.execute('''UPDATE Troskovi SET naziv=?, iznos=?, tip=?, namena=?, lokacija_id=?
                 WHERE id=?''', (data['naziv'], float(data['iznos']), data['tip'], data['namena'], lokacija_id, id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'})

@app.route('/top_lokacije', methods=['GET'])
def top_lokacije():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT Lokacije.naziv, COUNT(*) as broj
                 FROM Troskovi LEFT JOIN Lokacije ON Troskovi.lokacija_id = Lokacije.id
                 GROUP BY Lokacije.naziv ORDER BY broj DESC LIMIT 5''')
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/top3_lokacije4plus', methods=['GET'])
def top3_lokacije4plus():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT Lokacije.naziv, COUNT(*) as broj
                 FROM Troskovi LEFT JOIN Lokacije ON Troskovi.lokacija_id = Lokacije.id
                 GROUP BY Lokacije.naziv HAVING broj > 4
                 ORDER BY broj DESC LIMIT 3''')
    data = c.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

