from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('device_info.db') 
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS device_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        os_version TEXT,
        device_model TEXT,
        free_memory INTEGER
    )
    ''')
    conn.commit()
    conn.close()


def store_device_info(os_version, device_model, free_memory):
    conn = sqlite3.connect('device_info.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO device_info (os_version, device_model, free_memory)
    VALUES (?, ?, ?)
    ''', (os_version, device_model, free_memory))
    conn.commit()
    conn.close()


@app.route('/', methods=['POST'])
def receive_data():
    os_version = request.form.get('os_version')
    device_model = request.form.get('device_model')
    free_memory = request.form.get('free_memory')
    

    store_device_info(os_version, device_model, free_memory)
    
    print(f"OS Version: {os_version}")
    print(f"Device Model: {device_model}")
    print(f"Free Memory: {free_memory} MB")
    
    return 'Data received successfully', 200


@app.route('/data')
def display_data():
    conn = sqlite3.connect('device_info.db')
    c = conn.cursor()
    c.execute('SELECT * FROM device_info')
    rows = c.fetchall() 
    conn.close()
    

    return render_template('data_display.html', rows=rows)

if __name__ == '__main__':
    init_db() 
    app.run(host='0.0.0.0', port=5000)

