import requests
import base64
import random
import string
import urllib.parse

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_token()
        self.user_id = None
        self.redirect_uri = None

    def generate_random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def authenticate(self):
        state = self.generate_random_string(16)
        scope = 'user-read-private user-read-email user-top-read'
        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': scope,
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query_params)}"
        return auth_url

    def get_access_token(self, code):
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
        else:
            return None
    

    def get_token(self):
        # Encode the client ID and client secret
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

        # Set up the authorization options
        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }

        # Make the POST request to obtain the access token
        response = requests.post(auth_url, headers=headers, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            token = response.json()['access_token']
            print(f"Access Token: {token}")
            return token
        else:
            print(f"Failed to obtain access token, status code: {response.status_code}")
            print(response.json())
            return None

    def create_playlist(self, name, description):
        data = {
            "name": name,
            "description": description,
            "public": False
                }
        
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        self.request(url, data)

    def request(self, method, url, params=None, data=None, headers=None):
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.token}'
        
        response = requests.request(method, url, params=params, data=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.json())
            return None

# Example usage:
if __name__ == "__main__":
    # Replace with your actual Spotify API client ID and client secret
    client_id = '0e9026c74282412786b3c556db2b55ac'
    client_secret = '63922ecd0ed143a289181a5ca2d109ed'

    # Initialize the SpotifyAPI object
    spotify = SpotifyAPI(client_id, client_secret)

    # Define the URL of the Spotify API endpoint
    url = "https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy"

    # Make a GET request using the SpotifyAPI object
    response = spotify.request('GET', url)

    if response:
        # Print the status code of the response
        print("Status Code:", response)

        # Print the JSON response content
        print("Response Content:", response)
