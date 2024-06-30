from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import random
import string
import requests
import urllib.parse

app = Flask(__name__)
CORS(app)

CLIENT_ID = '8515fc5afe1f499d8411607a349a493d'
CLIENT_SECRET = 'd07aa9163cc340cb85f3c2ba3c78d1b2'
REDIRECT_URI = 'http://localhost:8888/callback'

access_token = None

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/login')
def login():
    state = generate_random_string(16)
    scope = 'user-read-private user-read-email user-top-read'
    query_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query_params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global access_token
    code = request.args.get('code')
    state = request.args.get('state')

    if code is None or state is None:
        return jsonify({"error": "Missing code or state"}), 400

    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return redirect('http://localhost:3000')  # Redirect to the React frontend
    else:
        return jsonify({"error": "Failed to get access token"}), 400

@app.route('/get_token')
def get_token():
    global access_token
    if access_token:
        return jsonify({'token': access_token})
    else:
        return jsonify({'error': 'No access token available'}), 400

@app.route('/get_top_artists')
def get_top_artists():
    global access_token
    if not access_token:
        return jsonify({'error': 'No access token available'}), 400

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=50', headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to retrieve top artists'}), response.status_code

if __name__ == '__main__':
    app.run(port=8888, debug=True)
