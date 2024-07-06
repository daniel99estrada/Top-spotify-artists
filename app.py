from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import random
import string
import requests
import urllib.parse
from spotify import SpotifyAPI
app = Flask(__name__)
CORS(app)

CLIENT_ID = '8515fc5afe1f499d8411607a349a493d'
CLIENT_SECRET = 'd07aa9163cc340cb85f3c2ba3c78d1b2'
REDIRECT_URI = 'http://localhost:8888/callback'

spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
access_token = None

@app.route('/login')
def login():
    auth_url = spotify.authenticate()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global access_token
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state:
        return jsonify({"error": "Missing code or state"}), 400
    
    access_token = spotify.get_access_token(code)

    if access_token:
        return redirect('http://localhost:3000')  # Redirect to the React frontend
    return jsonify({"error": "Failed to get access token"}), 400

@app.route('/get_token')
def get_token():
    token = spotify.get_access_token()
    if token:
        return jsonify({'token': token})
    return jsonify({'error': 'No access token available'}), 400

@app.route('/get_top_artists')
def get_top_artists():

    top_artists_long = spotify.get_top_artists(time_range='long_term', limit=10)['items']
    top_artists_medium = spotify.get_top_artists(time_range='medium_term', limit=10)['items']
    top_artists_short = spotify.get_top_artists(time_range='short_term', limit=10)['items']

    top_artists = {
        'long_term': [{'id': artist['id'], 'name': artist['name']} for artist in top_artists_long],
        'medium_term': [{'id': artist['id'], 'name': artist['name']} for artist in top_artists_medium],
        'short_term': [{'id': artist['id'], 'name': artist['name']} for artist in top_artists_short]
    }
    # playlist = spotify.create_playlist("test1", "Test playlistt functionalities")
    # print(f"ID: {playlist['id']}, Owner: {playlist['name']}")
    return jsonify(top_artists)
if __name__ == '__main__':
    app.run(port=8888, debug=True)