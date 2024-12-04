import subprocess
import os
import json

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

def run_command(command):
    """
    Run a terminal command and print its output.

    Args:
        command (str): The command to execute in the terminal.

    Returns:
        str: The standard output of the command.
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pretty_json = prettify_json(result.stdout)
        print("Command Output:")
        print(pretty_json)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error while executing command:")
        print(e.stderr)
        return e.stderr
    
def parse_json(output):
    """
    Parse JSON

    Args:
        output (str): JSON string to parse.

    Returns:
        dict: The parsed JSON as a Python dictionary, or None if parsing fails.
    """
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None
    
def prettify_json(json_string):
    """
    Prettify JSON

    Args:
        json_string (str): JSON string to prettify.

    Returns:
        str: The prettified JSON string.
    """
    try:
        parsed_json = json.loads(json_string)
        return json.dumps(parsed_json, indent=4)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None
    
def get_access_token():
    """
    Get an access token from the Spotify API, lasts for 1 hour.

    Returns:
        str: The access token.
    """
    get_access_token_command = f"curl -X POST \"https://accounts.spotify.com/api/token\" -H \"Content-Type: application/x-www-form-urlencoded\" -d \"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}\""
    output_json = run_command(get_access_token_command)
    parsed_json = parse_json(output_json)

    if parsed_json:
        return parsed_json.get("access_token")
    
    return None

def get_artist(artist_id, access_token):
    """
    Get an artist from the Spotify API.

    Args:
        artist_id (str): The Spotify ID of the artist.

    Returns:
        dict: The artist data.
    """

    get_artist_command = f"curl -X GET \"https://api.spotify.com/v1/artists/{artist_id}\" -H \"Authorization: Bearer {access_token}\""
    output_json = run_command(get_artist_command)
    pretty_json = prettify_json(output_json)
    return pretty_json


if __name__ == "__main__":
    access_token = get_access_token()
    print(f'Access Token: {access_token}')
    get_artist("246dkjvS1zLTtiykXe5h60", access_token)
    # https://open.spotify.com/artist/246dkjvS1zLTtiykXe5h60?si=VIxUc370QGOeRbWSsoN4NA