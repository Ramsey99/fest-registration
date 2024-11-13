from flask import Flask, render_template, request, url_for, redirect, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import os
import uuid  # Import for unique filenames
from web3 import Web3
import logging  # Import logging for error handling

# Initialize the app and CORS
app = Flask(__name__)
CORS(app)

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size: 16MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database and Blockchain configuration from environment variables
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'event_database'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD')  # Recommend using a secure secrets manager
}

blockchain_url = os.environ.get('BLOCKCHAIN_URL', 'http://127.0.0.1:8545')
web3 = Web3(Web3.HTTPProvider(blockchain_url))
contract_address = os.environ.get('CONTRACT_ADDRESS')
contract_abi = [...]  # Contract ABI array

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Function to establish a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        logging.error(f"Database connection error: {e}")
    return None

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Fetch form data
        roll = request.form['roll']
        fullname = request.form['fullname']
        email = request.form['email']
        phno = request.form['phno']
        stream = request.form['stream']
        event = request.form['event']

        # Validate inputs
        if not all([roll, fullname, email, phno, stream, event]):
            return jsonify({"error": "All fields are required"}), 400

        # Handle file upload securely
        profile_pic = request.files.get('profile')
        filename = None
        if profile_pic:
            filename = f"{uuid.uuid4()}_{profile_pic.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_pic.save(filepath)

        # Create a database connection
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        with connection.cursor() as cursor:
            add_registration_proc = "CALL add_registration(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(add_registration_proc, (roll, fullname, email, phno, stream, event, filename))
            connection.commit()

        return redirect(url_for('success'))

    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error occurred."}), 500

    except Exception as e:
        logging.error(f"General error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/see_details.html')
def see_details():
    connection = create_connection()
    rows = []
    event_filter = request.args.get('event')
    search_query = request.args.get('search')

    if connection:
        try:
            with connection.cursor() as cursor:
                # Secure parameterized query
                query = "SELECT * FROM registrations WHERE event = %s" if event_filter else "SELECT * FROM registrations"
                params = [event_filter] if event_filter else []

                if search_query:
                    query += " AND fullname LIKE %s"
                    params.append(f"%{search_query}%")

                cursor.execute(query, params)
                rows = cursor.fetchall()

        except Error as e:
            logging.error(f"Error fetching details: {e}")
            return jsonify({"error": "An error occurred while fetching details."}), 500

        finally:
            connection.close()

    return render_template('see_details.html', rows=rows)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/index.html', methods=['GET'])
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
