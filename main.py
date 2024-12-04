from http import HTTPStatus
import os
import json
import requests
from json_utils import parse_json, prettify_json

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
    
def get_access_token():
    """
    Get an access token from the Spotify API, lasts for 1 hour.

    Returns:
        str: The access token.
    """

    # Define API endpoint and data
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Send POST request to get access token
    response = requests.post(url, headers=headers, data=data)

    # Check the response status and print the token
    if response.status_code == HTTPStatus.OK:
        access_token = response.json().get('access_token')
        return access_token
    else:
        return str('Failed to get access token:', response.status_code, response.text)

def get_artist_by_id(artist_id, access_token):
    """
    Get an artist from the Spotify API.

    Args:
        artist_id (str): The Spotify ID of the artist.

    Returns:
        dict: The artist data.
    """

    # Define the API endpoint and headers
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request to get artist information
    response = requests.get(url, headers=headers)

    # Check the response status and print the artist info
    if response.status_code == HTTPStatus.OK:
        artist_data = response.json()
        pretty_data = prettify_json(artist_data)
        print(pretty_data)
    else:
        print('Failed to get artist data:', response.status_code, response.text)

def search_artist_by_name(name, access_token):
    """
    Search for an artist by name using the Spotify API.

    Args:
        name (str): The name of the artist to search for.

    Returns:
        dict: The artist data.
    """

    # Define the API endpoint and headers
    formatted_name = name.replace(' ', '+')
    url = f'https://api.spotify.com/v1/search?q={formatted_name}&type=artist&limit=1'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == HTTPStatus.OK:
        if len(response.json().get('artists').get('items')) == 0:
            print('No artist found.')
        else:
            artist = response.json().get('artists').get('items')[0]
            pretty_data = prettify_json(artist)
            print(pretty_data)


if __name__ == "__main__":
    access_token = get_access_token()
    print(f'Access Token: {access_token}')
    # get_artist_by_id("246dkjvS1zLTtiykXe5h60", access_token)
    search_artist_by_name("Post Malone", access_token)