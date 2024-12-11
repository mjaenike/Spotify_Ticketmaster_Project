##########################################################
"""
fetch_spotify_data.py

Handles Spotify API integration to fetch user's top artists. 
This includes obtaining access tokens, managing authentication, 
and returning artist data as a pandas DataFrame.

Functions:
- get_auth_code: Starts the OAuth process to get an authorization code.
- get_access_token: Exchanges the auth code for an access token.
- get_top_artists: Retrieves the user's top Spotify artists.

Dependencies:
- Requests
- Python-dotenv for secure credential management.
"""
##########################################################

# library imports
import requests
import base64
import webbrowser
from urllib.parse import urlencode
from flask import Flask, request
import threading
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
auth_code = None

app = Flask(__name__)

@app.route('/callback')
def callback():
    global auth_code
    auth_code = request.args.get('code')
    return 'Authorization code received. You can close this window now.'

def run_server():
    app.run(port=8890)

def get_auth_code():
    global auth_code
    # Start Flask server in a new thread
    threading.Thread(target=run_server).start()
    
    # Step 1: Authorization
    auth_headers = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": "user-top-read"
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)
    webbrowser.open(auth_url)
    
    # Wait for the authorization code to be set
    while auth_code is None:
        pass

    return auth_code

def get_access_token(auth_code):
    encoded_credentials = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode("utf-8")

    token_headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    # Handle possible errors
    if r.status_code != 200:
        print("Error in token request.")
        print(r.json())
        exit()

    token_response = r.json()
    if 'access_token' not in token_response:
        print("Access token not found in the response.")
        exit()

    token = token_response["access_token"]
    refresh_token = token_response.get("refresh_token", "")
    expires_in = token_response["expires_in"]
    print(f"Token: {token}")
    print(f"Refresh Token: {refresh_token}")
    print(f"Token Expires In: {expires_in} seconds")
    
    return token, refresh_token, expires_in

def get_top_artists():
    auth_code = get_auth_code()
    token, refresh_token, expires_in = get_access_token(auth_code)

    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = 'https://api.spotify.com/v1/me/top/artists'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        artists = data.get('items', [])
        
        # Convert to DataFrame
        artist_df = pd.DataFrame(artists)
        if not artist_df.empty:
            artist_df = artist_df[['name', 'id', 'popularity', 'genres']]
            
            # Save to CSV
            os.makedirs('data', exist_ok=True)  # Ensure the 'data' folder exists
            artist_df.to_csv('data/top_artists.csv', index=False)
        
        return artist_df
    else:
        print(f"Error fetching top artists: {response.status_code} - {response.text}")
        return pd.DataFrame()

def main() -> None:
    top_artists_df = get_top_artists()
    print(top_artists_df)

if __name__ == "__main__":
    main()