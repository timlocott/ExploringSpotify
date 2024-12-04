import json

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