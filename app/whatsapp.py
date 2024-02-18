# app/whatsapp.py
from fastapi import HTTPException
from models import UserSession
import requests


sessions = {}

async def handle_webhook():
    # Handle incoming messages from WhatsApp
    # Update sessions and return appropriate responses
    pass

async def register_for_event(event_name: str):
    # Register users for events
    # Check if user is already registered
    # Update session and return appropriate responses
    pass


async def call_whatsapp_api(url: str, token: str, body_json: dict) -> dict:
    """
    Calls WhatsApp API using HTTP POST method.

    Args:
        url (str): The URL of the WhatsApp API endpoint.
        token (str): The authentication token required by the API.
        body_json (dict): The JSON payload to be sent in the request body.

    Returns:
        dict: The response JSON returned by the WhatsApp API.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=body_json, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        print(f"Error occurred while making request: {e}")
        return None

#call_whatsapp_api("https://graph.facebook.com/v18.0/202554606283438/messages","EAAKNYZACUTs0BO98PxSvkgmJtGZAvmEkRQqsevRvuzVJO0us0sXLDs6pgQ8O0OANWhOllSFRAO5ELmU8wb9DMzFxqA744IWaD98JZATwdS9NOIGRayKJ1vcD0tsjEfa3yQbZAcHuqMdFfNnf2AX8ZAeEK4ha9qly6llEbIWhHoy5NthZA0YgWqehFAKgSRCZCDgrfTkmnhfVBaKu0IjbKYZD",body)