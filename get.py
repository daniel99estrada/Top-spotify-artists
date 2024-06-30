import requests
from spotify_token import get_token  # Assuming this function exists and retrieves the token

# Define the URL of the Spotify API endpoint
url = "https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy"

# Call get_token function to obtain the access token
access_token = get_token()

# Check if access_token is None (indicating an error in token retrieval)
if access_token is None:
    print("Failed to obtain Spotify access token.")
else:
    # Define the headers with the Bearer token
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    # Make the GET request to the Spotify API with the headers
    response = requests.get(url, headers=headers)

    # Print the status code of the response
    print("Status Code:", response.status_code)

    # Print the JSON response content
    print("Response Content:", response.json())
