from flask import Flask, render_template, request, url_for, redirect, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MySQL database configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),  # Default to localhost for local testing
    'database': os.environ.get('DB_NAME', 'event_database'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'anuradha')
}

# Function to establish a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to close a MySQL connection and cursor
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
        # Get form data
        roll = request.form['roll']
        fullname = request.form['fullname']
        email = request.form['email']
        phno = request.form['phno']
        stream = request.form['stream']
        event = request.form['event']

        # Validate inputs
        if not all([roll, fullname, email, phno, stream, event]):
            return jsonify({"error": "All fields are required"}), 400

        # Fetch file input correctly (if applicable)
        profile_pic = request.files.get('profile')  # Use get to avoid KeyError
        
        # Check if file is uploaded
        if profile_pic:
            # Save the file
            filename = f"{roll}_{profile_pic.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_pic.save(filepath)

        # Create a database connection
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
        return jsonify({"error": "An error occurred."}), 500

    finally:
        close_connection(connection, cursor)

@app.route('/see_details.html')
def see_details():
    connection = create_connection()
    cursor = None

    if connection:
        try:
            cursor = connection.cursor()
            select_query = "SELECT * FROM registrations"
            cursor.execute(select_query)
            rows = cursor.fetchall()
            return render_template('see_details.html', rows=rows)

        except Error as e:
            print(f"Error occurred while fetching details: {e}")
            return jsonify({"error": "An error occurred while fetching details."}), 500

        finally:
            close_connection(connection, cursor)

    return jsonify({"error": "Error occurred. Please try again later."}), 500

# Route to serve the success.html page
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/index.html', methods=['GET'])
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
