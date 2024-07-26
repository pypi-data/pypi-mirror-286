import os
from dotenv import load_dotenv

def load_auth_token():
    # Load the .env file
    load_dotenv()
    
    # Get the AUTH_TOKEN from the .env file
    auth_token = os.getenv('AUTH_TOKEN')
    
    if not auth_token:
        print("Error: AUTH_TOKEN not found in .env file.")
        return None
    
    return auth_token

def get_headers():
    auth_token = load_auth_token()
    headers = {}
    if auth_token:
        headers['X-API-AUTH'] = auth_token
    return headers