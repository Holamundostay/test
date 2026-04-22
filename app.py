from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  appreciation TEXT,
                  negative TEXT)''')
    conn.commit()
    conn.close()

@app.route('/save', methods=['POST'])
def save_entry():
    data = request.get_json()
    appreciation = data.get('appreciation')
    negative = data.get('negative')
    date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute("INSERT INTO entries (date, appreciation, negative) VALUES (?, ?, ?)",
              (date, appreciation, negative))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/entries', methods=['GET'])
def get_entries():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute("SELECT date, appreciation, negative FROM entries ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    entries = [{'date': row[0], 'appreciation': row[1], 'negative': row[2]} for row in rows]
    return jsonify(entries)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)