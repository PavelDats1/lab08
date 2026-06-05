from flask import Flask, request, render_template_string
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'messages_db')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
            conn.commit()
            cursor.close()
            conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT message, created_at FROM messages ORDER BY created_at DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head><title>Message Board</title></head>
    <body>
        <h1>Message Board</h1>
        <form method="post">
            <input type="text" name="message" placeholder="Enter your message" size="50" required>
            <button type="submit">Send</button>
        </form>
        <h2>Messages:</h2>
        <ul>
        {% for msg, date in messages %}
            <li><strong>{{ date }}</strong>: {{ msg }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    '''
    from flask import render_template_string
    return render_template_string(html, messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
