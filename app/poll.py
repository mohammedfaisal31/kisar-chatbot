import gspread
import os
from dotenv import load_dotenv
import schedule
import time
from userUtils import *
from utils import sendPaymentLink
from db import get_db

# Load environment variables
load_dotenv()

# Replace with your sheet ID
SHEET_ID = os.getenv('SHEET_ID')


db = get_db()
# Authorize access to Google Sheets
gc = gspread.service_account(filename='./gcloud_cred.json')
worksheet = gc.open_by_key(SHEET_ID).sheet1

def checkRegistrationAndSendPaymentLink():
    try:
        # Filter data based on conditions
        data = worksheet.get_all_records()
        
        # Update records and call sendPaymentLink
        for i, row in enumerate(data):
            if row["Timestamp"] != "" and row["Payment Link Sent"] != "TRUE" :
                _package_id = 0
                if "NR1-1" in row["Select the package"]:
                    _package_id = 1
                elif "NR1-2" in row["Select the package"]:
                    _package_id = 2
                elif "SO1-1" in row["Select the package"]:
                    _package_id = 3
                elif "SO1-2" in row["Select the package"]:
                    _package_id = 4
                elif "DO1-1" in row["Select the package"]:
                    _package_id = 5
                elif "DO1-2" in row["Select the package"]:
                    _package_id = 6
                else:
                    _package_id = 0
                print(_package_id)
                
                _created_user = create_user(row["Honorific"],row["First Name"],row["Middle Name"],row["Last Name"],row["Email"],row["Phone number"],row["Category"],_package_id,row["Medical Council Number"],row["City"],row["State"],row["Type Of Visitor"],db)
                phone_number = row['Phone number']
                _user_session = checkUserSessionNumber(phone_number,db)
                print(_user_session)
                if _created_user:
                    _send_payment_link_code = sendPaymentLink("91"+str(phone_number))
                    if _send_payment_link_code == 200:
                        _update_session_code = updateUserSession(phone_number,2,db)
                        if _update_session_code:
                            worksheet.update_cell(i+2, 17, "TRUE")
                            print(f"Payment link sent and record updated for phone number: {phone_number}")

    except Exception as e:
        print(f"Error updating records: {e}")

# Schedule the function to run every 5 seconds
schedule.every(5).seconds.do(checkRegistrationAndSendPaymentLink)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
