import requests
import base64

def get_token(): 
    # Define client ID and client secret
    client_id = '0e9026c74282412786b3c556db2b55ac'
    client_secret = '63922ecd0ed143a289181a5ca2d109ed'

    # Encode the client ID and client secret
    auth_string = f"{client_id}:{client_secret}"
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
