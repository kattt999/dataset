import time
import json
import sqlite3
from collections import defaultdict, deque
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Initialize SQLite database
db_connection = sqlite3.connect('data.db')
db_cursor = db_connection.cursor()
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source TEXT,
        value REAL
    )
''')
db_connection.commit()

# Data processing function
def process_data(data):
    timestamp = data['timestamp']
    source = data['source']
    value = data['value']
    
    # Store data in SQLite database
    db_cursor.execute('INSERT INTO data (timestamp, source, value) VALUES (?, ?, ?)',
                      (timestamp, source, value))
    db_connection.commit()

# Data ingestion API
@app.route('/ingest', methods=['POST'])
def ingest_data():
    data = request.json
    process_data(data)
    return jsonify({'message': 'Data ingested successfully'})

# Data retrieval API
@app.route('/metrics/<source>', methods=['GET'])
def get_metrics(source):
    db_cursor.execute('SELECT AVG(value), SUM(value), COUNT(value) FROM data WHERE source = ?', (source,))
    average, total_sum, count = db_cursor.fetchone()
    return jsonify({
        'average': average,
        'sum': total_sum,
        'count': count
    })

# Long polling for real-time updates
listeners = defaultdict(list)
@app.route('/listen/<source>')
def listen_data(source):
    queue = deque()
    listeners[source].append(queue)
    try:
        while True:
            if queue:
                data = queue.popleft()  # Get the oldest data
                yield f"data: {json.dumps(data)}\n\n"
            else:
                time.sleep(1)  # Wait before checking again
    except GeneratorExit:
        listeners[source].remove(queue)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
