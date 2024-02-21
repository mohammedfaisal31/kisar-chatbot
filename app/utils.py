from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
from db import create_db_connection

load_dotenv()
whatsapp_token = os.getenv("WHATSAPP_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")

class WhatsAppMessage(BaseModel):
    messaging_product: str
    to: str
    text: dict

whatsapp_token = "EAAMwP9BDHBABO6fx2w6QU6vJMo2rsAAPa2ZBVYZCYB1jwBhj7KqcJS8gZCxrhS5IBxyC5SQfD7YhinwisGOHPBprIa35Sv54CFazcK79aL8Ugrs75hbdOff7XtxveZBJ2365VmxIB7WjckU5kJYqaHDoN4eSZBnNC8oZA5tQL2LPCoDePPKutAJXdy4ideRFEpzcLfhBU5EeTT95f29urwZCsV8irUZD"

def processWhatsAppMessage(body):
    if "object" in body:
        if (
            "entry" in body and body["entry"]
            and "changes" in body["entry"][0] and body["entry"][0]["changes"]
            and "value" in body["entry"][0]["changes"][0] and body["entry"][0]["changes"][0]["value"]
            and "messages" in body["entry"][0]["changes"][0]["value"] and body["entry"][0]["changes"][0]["value"]["messages"]
        ):
            phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            from_number = body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            
            
            if body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "text":
                msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if msg_body == "Hi":
                    # response_welcome = sendWelcomeMessage(from_number)
                    # if response_welcome:
                    #     
                    send_plans(from_number)
                else:
                    response = sendTryAgainMessage(from_number)
                    return response
            elif body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "interactive":
                if body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["type"] == "list_reply":
                    user_selection = body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]

                    if user_selection["id"] == "1":
                        sendPackageConfirmMessage(from_number,"Non residential package Price - 12000")
                    elif user_selection["id"] == "2":
                        sendPackageConfirmMessage(from_number,"Single Occupancy for One day Price - 25000")
                    elif user_selection["id"] == "3":
                        sendPackageConfirmMessage(from_number,"Single Occupancy for Two days Price - 37000")
                    elif user_selection["id"] == "4":
                        sendPackageConfirmMessage(from_number,"Double Occupancy for One day Price - 21000")
                    elif user_selection["id"] == "5":
                        sendPackageConfirmMessage(from_number,"Double Occupancy for One day Price - 29000")
                    else :
                        print("Invalid!")
                elif body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["type"] == "button_reply":
                    user_selection = body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]

                    if user_selection["title"] == "Yes":
                        sendPaymentLink(from_number)
                    elif user_selection["title"] == "No":
                        sendConversationTerminateMessage(from_number)
                    else :
                        print("Invalid!")
                                    
def sendPaymentLink(to):
    message = WhatsAppMessage(
                        messaging_product="whatsapp",
                        to=to,
                        text={"body": f"Please proceed with payment..Click the link below to pay"}
                    )
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=message.model_dump(), headers=headers)
    response.raise_for_status()  
    return response
   
def sendConversationTerminateMessage(to):
    message = WhatsAppMessage(
                        messaging_product="whatsapp",
                        to=to,
                        text={"body": f"Conversation terminated"}
                    )
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=message.model_dump(), headers=headers)
    response.raise_for_status()  
    return response

def sendWelcomeMessage(to):
    message = WhatsAppMessage(
                        messaging_product="whatsapp",
                        to=to,
                        text={"body": f"Welcome to Registartion!"}
                    )
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=message.model_dump(), headers=headers)
    response.raise_for_status()  
    return response  

            
def sendPackageConfirmMessage(to, selection):

    

    payload = {
        "messaging_product":"whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": "Please confirm"
            },
            "body":{
                "text":f"Would you like to confirm your selection?\n {selection}"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "1",
                            "title": "Yes" 
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "2",
                            "title": "No" 
                        }
                    }
                ]
                
            }
        }
    }
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response      

def sendTryAgainMessage(to):
    message = WhatsAppMessage(
                        messaging_product="whatsapp",
                        to=to,
                        text={"body": f"Please type Hi to start a conversation"}
                    )
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=message.model_dump(), headers=headers)
    response.raise_for_status()  
    return response


def send_plans(to):
    packages = get_packages()
    formatted_packages = format_packages(packages)
    sections = [
        {
        "title": "Non Residential",
        "rows": [formatted_packages[0]]
        },
        {
        "title": "Single Occupancy",
        "rows": formatted_packages[1:3]
        },
        {
        "title": "Double Occupancy",
        "rows": formatted_packages[3:5]
        },
        
     ]
    
    payload = {
        "messaging_product":"whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Choose a package:"
            },
            "body":{
                "text":"Please select a package from the list below"
            },
            "footer": {
                "text": "Select a package from the list."
            },
            "action": {
                "button": "Select",
                "sections": sections
            }
        }
    }


    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages?access_token={whatsapp_token}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response

        
# Function to fetch package data from MySQL
def get_packages():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT package_id, package_name, package_price FROM packages")
    packages = cursor.fetchall()
    cursor.close()
    connection.close()
    return packages

# Function to format packages into the required JSON structure
def format_packages(packages):
    formatted_packages = []
    for package in packages:
        formatted_package = {
            "id": str(package[0]),  # Converting package_id to string as it's required to be unique
            "title": package[1],
            "description": f"Price: {package[2]}"
        }
        formatted_packages.append(formatted_package)
    return formatted_packages

        