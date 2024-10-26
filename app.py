from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import os
from web3 import Web3  # Import Web3 for Ethereum integration
import logging

app = Flask(__name__)
CORS(app)

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size: 16MB

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
logging.basicConfig(
    filename='bot.log',  # Log file name
    level=logging.INFO,   # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)
python
async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Please use the format: /convert <crypto> <currency> <amount>")
        return
    
    crypto = context.args[0].lower()
    currency = context.args[1].lower()
    amount = float(context.args[2])
    
    # Log the conversion request
    logging.info(f"User {update.message.from_user.id} requested conversion: {amount} {crypto} to {currency}")

    price = get_crypto_price(crypto, currency)
    if price != 'Price not available':
        converted_amount = price * amount
        await update.message.reply_text(f"{amount} {crypto.capitalize()} is worth {converted_amount} {currency.upper()}.")
    else:
        await update.message.reply_text('Price not available.')
async def show_crypto_details(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto_id: str, currency: str) -> None:
    await asyncio.sleep(1)  # Add a delay to avoid hitting rate limits
    details = get_crypto_details(crypto_id, currency)
    
    # Log the price check request
    logging.info(f"User {update.callback_query.from_user.id} checked price for {crypto_id} in {currency}")

    if details:
        price = details.get(currency, 'N/A')
        # (rest of your code)
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")
# MySQL database configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'event_database'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'anuradha') # write your own password
}

# Blockchain configuration
blockchain_url = os.environ.get('BLOCKCHAIN_URL', 'http://127.0.0.1:8545')  # Change this to your Ethereum node URL
web3 = Web3(Web3.HTTPProvider(blockchain_url))

# Smart contract ABI and address
contract_address = os.environ.get('CONTRACT_ADDRESS', '0xYourContractAddress')  # Replace with actual contract address
contract_abi = [
    # Add your contract ABI here
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to establish a MySQL connection

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

        # Fetch file input correctly
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
            raise Exception("Failed to connect to the database")  # Handle connection failure

        cursor = connection.cursor()

        # Call stored procedure to add registration, including the image file name
        add_registration_proc = "CALL add_registration(%s, %s, %s, %s, %s, %s, %s)"
        data = (roll, fullname, email, phno, stream, event, filename)
        cursor.execute(add_registration_proc, data)
        connection.commit()
        return redirect(url_for('success'))

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred."}), 500

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()  # Safely close the cursor if it was created
        if connection:
            connection.close()  # Safely close the connection if it was created

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
