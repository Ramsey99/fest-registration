from flask import Flask, render_template, request, url_for, redirect, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MySQL database configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'event_database'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Varsha@1605!!')
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        roll = request.form['roll']
        fullname = request.form['fullname']
        email = request.form['email']
        phno = request.form['phno']
        stream = request.form['stream']
        event = request.form['event']

        connection = create_connection()
        if connection is None:
            raise Exception("Failed to connect to the database")

        cursor = connection.cursor()
        add_registration_proc = "CALL add_registration(%s, %s, %s, %s, %s, %s)"
        data = (roll, fullname, email, phno, stream, event)
        cursor.execute(add_registration_proc, data)
        connection.commit()

        return redirect(url_for('success'))

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred."}), 500

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"error": "Duplicate entry occurred."}), 500

    finally:
        if connection:
            close_connection(connection, cursor)

@app.route('/see_details.html')
def see_details():
    connection = create_connection()
    cursor = None
    rows = []
    event_filter = request.args.get('event')
    search_query = request.args.get('search')

    if connection:
        try:
            cursor = connection.cursor()

            # Basic query
            select_query = "SELECT * FROM registrations WHERE 1=1"

            # Event filter
            if event_filter:
                select_query += f" AND event='{event_filter}'"

            # Search filter
            if search_query:
                select_query += f" AND fullname LIKE '%{search_query}%'"

            cursor.execute(select_query)
            rows = cursor.fetchall()

        except Error as e:
            print(f"Error occurred while fetching details: {e}")
            return jsonify({"error": "An error occurred while fetching details."}), 500

        finally:
            close_connection(connection, cursor)

    return render_template('see_details.html', rows=rows)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/index.html', methods=['GET'])
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
