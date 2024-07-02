import requests
import base64
import random
import string
import urllib.parse

class SpotifyAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.user_id = None

    def generate_random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def authenticate(self):
        state = self.generate_random_string(16)
        scope = 'playlist-modify-private playlist-modify-public user-read-private user-read-email user-top-read'
        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': scope,
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query_params)}"
        return auth_url

    def get_access_token(self, code=None):
        if self.access_token:
            return self.access_token

        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(token_url, data=token_data)

        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            return self.access_token
        return None

    def get_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(auth_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get('access_token')
        return None

    def create_playlist(self, name, description):
        data = {
            "name": name,
            "description": description,
            "public": False
        }

        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        return self.request('POST', url, data=data)

    def request(self, method, url, params=None, data=None, headers=None):
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.access_token}'

        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.request(method, url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        print(f"Request to {url} failed with status code {response.status_code}")
        print("Response content:", response.json())
        return None
        
    def get_top_artists(self, time_range='long_term', limit=50):
        url = f'https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}'
        response = self.request("GET", url)
        return response