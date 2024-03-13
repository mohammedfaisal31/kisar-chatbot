from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
from db import get_db
from userUtils import *
from packageUtils import *
from payment import createPaymentLink
from updatePaymentStatusInSheet import updatePaymentStatusInSheet
from typing import Dict
from qr import generate_pdf_with_qr_and_text

load_dotenv()
whatsapp_token = os.getenv("WHATSAPP_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")
url = os.getenv("WHATSAPP_API_URL")
host = os.getenv("HOST")
form_link = os.getenv("FORM_LINK")
db = get_db()

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
            
            
            # if body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "text":
            #     msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            #     if msg_body == "Hi" or msg_body == "hi":
            #         user = check_if_user_exists(from_number[2:],db)
            #         if user.user_session_number < 5:
            #             _send_welcome_code = sendWelcomeMessage(from_number,user)
            #             _update_session_code = update_user_session_number(from_number[2:],1,db)
            #             if _send_welcome_code == 200 and _update_session_code:
            #                 _send_plans_response = send_plans(from_number)
            #                 _update_session_code = update_user_session_number(from_number[2:],2,db)
            #                 if _send_plans_response == 200 and _update_session_code:
            #                     return True
            #         elif user == None:
            #             print("User not Registered")
            #             #Send Google form link
            #         else:
            #             print("User Already Registered")
            #     else:
            #         _try_again_response = sendTryAgainMessage(from_number)
            #         if _try_again_response == 200:
            #             return True
            # elif body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "interactive":
            #     if body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["type"] == "list_reply":
            #         user_selection = body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]

            #         confirmation_message = ""
            #         package_id = 0
            #         if user_selection["id"] == "1":
            #             confirmation_message = "*Non residential package* \n*Price*: ₹14,000"
            #             package_id = 1
            #         elif user_selection["id"] == "2":
            #             confirmation_message = "*Non residential package* With an accompanying peron \n*Total Price*: ₹26,000"
            #             package_id = 2
            #         elif user_selection["id"] == "3":
            #             confirmation_message = "*Residential package*\nSingle Occupancy for One day\n*Price*: ₹27,000"
            #             package_id = 3
            #         elif user_selection["id"] == "4":
            #             confirmation_message = "*Residential package*\nSingle Occupancy for Two days\n*Price*: ₹39,000"
            #             package_id = 4
            #         elif user_selection["id"] == "5":
            #             confirmation_message = "*Residential package*\Double Occupancy for One day\n*Price*: ₹23,000"
            #             package_id = 5
            #         elif user_selection["id"] == "6":
            #             confirmation_message = "*Residential package*\Double Occupancy for Two days\n*Price*: ₹31,000"
            #             package_id = 6
            #         else :
            #             print("Invalid!")
            #         _upadte_user_package_code = update_user_package_id(from_number[2:],package_id,db)
            #         if _upadte_user_package_code:
            #             _user_session_number = get_user_session_number(from_number[2:],db)
            #             if _user_session_number == 2:
            #                 _send_confirm_code = sendPackageConfirmMessage(from_number,confirmation_message)
            #                 if _send_confirm_code == 200:
            #                     _update_user_session_code = update_user_session_number(from_number[2:],3,db)
            #                     if _update_user_session_code:
            #                         return True
            # elif body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["type"] == "button_reply":
            #     user_selection = body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]

            #     if user_selection["id"] == "PS-1":
            #         _user_session_number = get_user_session_number(from_number[2:],db)
            #         if _user_session_number == 3:
            #             _send_payment_link_code = sendPaymentLink(from_number)
            #             _update_user_session_code = update_user_session_number(from_number[2:],4,db)
            #             if _update_user_session_code and _send_payment_link_code == 200:
            #                 return True
            #     elif user_selection["id"] == "PS-2":
            #         _user_session_number = get_user_session_number(from_number[2:],db)
            #         if _user_session_number == 3:
            #             _send_terminate_code = sendConversationTerminateMessage(from_number)
            #             if _send_terminate_code == 200:
            #                 _update_user_session_code = update_user_session_number(from_number[2:],0,db)
            #                 if _update_user_session_code:
            #                     return True
            if body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "button":
                if body["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["text"] == "Register Now":
                    user_session_number = checkUserSessionNumber(from_number[2:],db)
                    if user_session_number == 0:
                        _send_form = sendFormLink(from_number)
                        if _send_form == 200:
                            _update_session = updateUserSession(from_number[2:],1,db)
                            return _update_session
                    elif user_session_number == None:
                        _create_session = createUserSession(from_number[2:],db)
                        if _create_session:
                            _send_form = sendFormLink(from_number)
                            if _send_form == 200:
                                _update_session = updateUserSession(from_number[2:],1,db)
                                return _update_session
            if body["entry"][0]["changes"][0]["value"]["messages"][0]["type"] == "text":
                msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if msg_body == "Hi" or msg_body == "hi":
                    user_session_number = checkUserSessionNumber(from_number[2:],db)
                    if user_session_number == 0:
                        _send_form = sendFormLink(from_number)
                        if _send_form == 200:
                            _update_session = updateUserSession(from_number[2:],1,db)
                            return _update_session
                    elif user_session_number == None:
                        _create_session = createUserSession(from_number[2:],db)
                        if _create_session:
                            _send_form = sendFormLink(from_number)
                            if _send_form == 200:
                                _update_session = updateUserSession(from_number[2:],1,db)
                                return _update_session

            
                                    

   
def sendConversationTerminateMessage(to):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":f"Conversation terminated"
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def sendRegisterSucessMessage(to):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":f"*Congratulations!...*Your Registration was successful\nPlease wait while we fetch your receipt"
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def sendWelcomeMessage(to,user):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":f"Dear {user.user_first_name}, Welcome to Registration of South ISAR 2024!"
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def sendFormLink(to):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":f"Please Click the link below to register\n{form_link}\n\n --------\n*Note* : Once you have filled the form and submitted, Please come back to whatsapp to receive a payment link"
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code 

def sendRegisterTemplate(to):
    payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "template",
                "template": {
                "name": "south_isar",
                "language": {
                    "code": "en"
                },
                "components": [
                    {
                    "type": "header",
                    "parameters": [
                        {
                        "type": "image",
                        "image": {
                            "link": f"{host}/template/banner.jpg"
                        }
                        }
                    ]
                    },
                    {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {
                        "type": "payload",
                        "payload": "PAYLOAD"
                        }
                    ]
                    }
                ]
                }
            }
    print(f"{host}/template/banner.jpg")
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code 



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
                            "id": "PS-1",
                            "title": "Yes" 
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "PS-2",
                            "title": "No" 
                        }
                    }
                ]
                
            }
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def sendTryAgainMessage(to):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":"Please Type Hi to start a conversation"
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def sendDocument(to,payment_id):
    print(to)
    print(f"{host}/pdfs/{payment_id}.pdf")
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "document",
        "document": {
            "link": f"{host}/pdfs/{payment_id}.pdf"
    }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code

def send_plans(to):
    packages = get_packages()
    sections = [{"title":"Non-Residential Packages","rows":[]},{"title":"Residential Packages","rows":[]},]
    for package in packages:
        
        if package.package_id == 1:
            row = {
                        "id": package.package_id,
                        "title": f"{package.package_title} ",
                        "description": f"Price : ₹{package.package_price}/-"
                    }
                
            sections[0]["rows"].append(row)
        elif package.package_id == 2:
            row = {
                        "id": package.package_id,
                        "title": f"{package.package_title} ",
                        "description": f"₹14000 + Accompanying person(₹12000) Total: ₹{package.package_price}/-"
                    }
                
                
            sections[0]["rows"].append(row)
        else:
            row = {
                    "id": package.package_id,
                    "title": f"{package.package_occupancy} Occupancy ",
                    "description": f" {package.package_duration} package : ₹{package.package_price}/-"
                }
            sections[1]["rows"].append(row)
        
        
            

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Choose a package:"
            },
            "body": {
                "text": "Please select a package from the list below"
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
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.status_code
        

def sendPaymentLink(to):
    user = check_if_user_exists(to[2:],db)
    paymentDetails = {}
    if user != None:
        package = get_package_by_id(user.user_package_id)
        paymentDetails["amount"] = package.package_price
        paymentDetails["buyer_name"] = f"{user.user_honorific}.{user.user_first_name} {user.user_last_name}"
        if package.package_id == 1:
            paymentDetails["purpose"] =  f"{package.package_title}"

        elif package.package_id == 2:
            paymentDetails["purpose"] = f"{package.package_title} + Accompanying person"
                    
        else:
            paymentDetails["purpose"] = f"{package.package_title} {package.package_occupancy} Occupancy {package.package_duration} package "
        paymentDetails["phone"] = user.user_phone 
        paymentDetails["email"] = user.user_email

    _create_payment_link_response = createPaymentLink(paymentDetails)
    paymentLink = ""
    if _create_payment_link_response:
        paymentLink = _create_payment_link_response["payment_request"]["longurl"]
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text":{
            "body":f"Please Click the link below to pay\n{paymentLink}\n\n --------\n*Note* : Once the payment is complete, You will receive a receipt/badge here"
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.status_code
        
def processPayment(data: Dict[str, str]):
    if data["status"] == "Credit":
        buyer_phone = data["buyer_phone"][3:]
        whatsapp_phone = data["buyer_phone"][1:]
        print(whatsapp_phone)
        _updatePaymentStatus = updateUserPaymentDetails(buyer_phone,data["payment_id"],"SUCCESS",db)
        if _updatePaymentStatus:
            _updatePaymentInSheet = updatePaymentStatusInSheet(buyer_phone,"TRUE")
            user = check_if_user_exists(buyer_phone,db)
            if user:
                user_middle_name = user.user_middle_name
                if user_middle_name is None or user_middle_name == "":
                    user_middle_name = ""
                payment_id = data["payment_id"]
                pdf_path = f"./pdfs/{payment_id}.pdf"
                if user.user_category == "Delegate":
                    _gen_pdf = generate_pdf_with_qr_and_text("./template/delegate_500.png", pdf_path, data["payment_id"], user.user_honorific,user.user_first_name ,user_middle_name, user.user_last_name,user.user_city,user.user_state_of_practice)
                    if _gen_pdf:
                        _user_session_number = checkUserSessionNumber(buyer_phone,db)
                        if _user_session_number == 2:
                            _send_success = sendRegisterSucessMessage(whatsapp_phone)
                            _send_Doc = sendDocument(whatsapp_phone,data["payment_id"])
                            if _send_success == 200 and _send_Doc == 200:
                                _update_user_session = updateUserSession(buyer_phone,3,db)
                                if _user_session_number:
                                    return True

                if user.user_category == "Faculty":
                    _gen_pdf = generate_pdf_with_qr_and_text("./template/faculty_500.png", pdf_path, data["payment_id"], user.user_honorific,user.user_first_name ,user_middle_name, user.user_last_name,user.user_city,user.user_state_of_practice)
                    if _gen_pdf:
                        _user_session_number = checkUserSessionNumber(buyer_phone,db)
                        if _user_session_number == 2:
                            _send_success = sendRegisterSucessMessage(whatsapp_phone)
                            _send_Doc = sendDocument(whatsapp_phone,data["payment_id"])
                            if _send_success == 200 and _send_Doc == 200:
                                _update_user_session = updateUserSession(buyer_phone,3,db)
                                if _user_session_number:
                                    return True
                    
            


