from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'database': 'event_database',
    'user': 'root',
    'password': 'anuradha'
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
    # Get form data
    roll = request.form['roll']
    fullname = request.form['fullname']
    email = request.form['email']
    phno = request.form['phno']
    stream = request.form['stream']
    event = request.form['event']

    connection = create_connection()
    cursor = None

    if connection:
        try:
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Use stored procedure to insert form data into the 'registrations' table
            add_registration_proc = "CALL add_registration(%s, %s, %s, %s, %s, %s)"
            data = (roll, fullname, email, phno, stream, event)
            cursor.execute(add_registration_proc, data)

            # Commit the changes to the database
            connection.commit()

            # After processing the form data, redirect to the success page.
            return redirect(url_for('success'))

        except Error as e:
            # Log the error and display a message for debugging
            print(f"Error occurred during form submission: {e}")
            return "An error occurred during form submission. Please try again later."

        finally:
            # Close the cursor and connection in the finally block
            close_connection(connection, cursor)

    # If there was an error or the connection could not be established,
    # redirect to the failure page or show an error message.
    return "Error occurred. Please try again later."

@app.route('/see_details.html')
def see_details():
    connection = create_connection()
    cursor = None

    if connection:
        try:
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # SQL query to select all rows from the 'registrations' table
            select_query = "SELECT * FROM registrations"
            cursor.execute(select_query)

            # Fetch all rows from the result set
            rows = cursor.fetchall()

            # Render the see_details.html template and pass the 'rows' data to the template
            return render_template('see_details.html', rows=rows)

        except Error as e:
            # Log the error and display a message for debugging
            print(f"Error occurred while fetching details: {e}")
            return "An error occurred while fetching details. Please try again later."

        finally:
            # Close the cursor and connection in the finally block
            close_connection(connection, cursor)

    # If there was an error or the connection could not be established,
    # redirect to the failure page or show an error message.
    return "Error occurred. Please try again later."

# Route to serve the success.html page
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/index.html', methods=['GET'])
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
