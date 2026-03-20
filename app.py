from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from datetime import datetime

# Initialize the Flask web server
app = Flask(__name__)
# Enable CORS so your mobile webpage is allowed to talk to this server
CORS(app) 

# Connect to Google Sheets using the bot credentials
gc = gspread.service_account(filename='credentials.json')
# Open the specific sheet by its exact name
sheet = gc.open("NFC_Attendance").sheet1

# Create an endpoint that listens for POST requests
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    # Extract the JSON data sent from the mobile phone
    data = request.json
    student_id = data.get('student_id')
    auth_status = data.get('biometric_verified')
    
    # If the phone says the fingerprint failed, reject the request
    if not auth_status:
        return jsonify({"error": "Biometric verification failed"}), 401

    # Get the exact current date and time
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")
    
    # Format the data into a list representing a row in Excel
    row = [student_id, date_string, time_string, "Present"]
    
    # Append the row to the bottom of the Google Sheet
    sheet.append_row(row)
    
    # Send a success message back to the phone
    return jsonify({"message": "Attendance Recorded!"}), 200

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)