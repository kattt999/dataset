from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            user_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    time = data.get('time')
    duration = data.get('duration')
    user_id = 1  # In a real app, you'd get the user ID from the session

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (title, description, date, time, duration, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                   (title, description, date, time, duration, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Event created successfully"})

@app.route('/user_events', methods=['GET'])
def user_events():
    user_id = 1  # In a real app, you'd get the user ID from the session

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, date, time FROM events WHERE user_id = ?', (user_id,))
    events = cursor.fetchall()
    conn.close()

    event_list = [{"id": event[0], "title": event[1], "date": event[2], "time": event[3]} for event in events]
    return jsonify({"events": event_list})

@app.route('/update_event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    time = data.get('time')
    duration = data.get('duration')

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE events SET title=?, description=?, date=?, time=?, duration=? WHERE id=?',
                   (title, description, date, time, duration, event_id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Event with ID {event_id} updated successfully"})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
