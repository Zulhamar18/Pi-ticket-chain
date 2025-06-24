from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os
import simplejson as json
import requests
import random

# Load .env variables
load_dotenv()
API_KEY = os.getenv(drf9t678txi3dsatyhvb7o9fcqmvwj5wlkgy4mebxy3ytjxkue64jx0vf2elqgrm)

# Setup Flask app
app = Flask(__name__)
Bootstrap(app)

# Pi Network API Headers
header = {
    'Authorization': f"Key {drf9t678txi3dsatyhvb7o9fcqmvwj5wlkgy4mebxy3ytjxkue64jx0vf2elqgrm}"
}

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Random Quote Generator
@app.route('/get_quote')
def get_quote():
    try:
        with open('quotes.txt', 'r') as f:
            quotes = f.readlines()
        return random.choice(quotes)
    except Exception as e:
        return f"Error reading quotes.txt: {str(e)}"

# Back Page
@app.route('/back')
def back():
    return render_template('back.html')

# Payment Approval
@app.route('/payment/approve', methods=['POST'])
def approve():
    access_token = request.form.get('accessToken')
    payment_id = request.form.get('paymentId')
    user_header = {
        'Authorization': f"Bearer {access_token}"
    }
    
    approve_url = f"https://api.minepi.com/v2/payments/{payment_id}/approve"
    response = requests.post(approve_url, headers=header)

    # Get user info
    user_url = "https://api.minepi.com/v2/me"
    user_response = requests.get(user_url, headers=user_header)
    user_json = json.loads(user_response.text)

    return response.text

# Payment Completion
@app.route('/payment/complete', methods=['POST'])
def complete():
    access_token = request.form.get('accessToken')
    payment_id = request.form.get('paymentId')
    txid = request.form.get('txid')

    user_header = {
        'Authorization': f"Bearer {access_token}"
    }
    complete_url = f"https://api.minepi.com/v2/payments/{payment_id}/complete"
    data = {'txid': txid}
    response = requests.post(complete_url, headers=header, data=data)

    return response.text

# Payment Cancellation
@app.route('/payment/cancel', methods=['POST'])
def cancel():
    payment_id = request.form.get('paymentId')
    cancel_url = f"https://api.minepi.com/v2/payments/{payment_id}/cancel"
    response = requests.post(cancel_url, headers=header)
    return response.text

# Payment Error (also cancels)
@app.route('/payment/error', methods=['POST'])
def error():
    payment_id = request.form.get('paymentId')
    error_url = f"https://api.minepi.com/v2/payments/{payment_id}/cancel"
    response = requests.post(error_url, headers=header)
    return response.text

# Get User Info from Pi Network
@app.route('/me', methods=['POST'])
def getme():
    user_url = "https://api.minepi.com/v2/me"
    response = requests.post(user_url, headers=header)
    return response.text

# Run server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
