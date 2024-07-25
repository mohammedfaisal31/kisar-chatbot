import gspread
import os
from dotenv import load_dotenv
import schedule
import time
from userUtils import *
from db import get_db

# Load environment variables
load_dotenv()

# Replace with your sheet ID
SHEET_ID = os.getenv('SHEET_ID')



# Authorize access to Google Sheets
gc = gspread.service_account(filename='./gcloud_cred.json',scopes=['https://spreadsheets.google.com/feeds'])
worksheet = gc.open_by_key(SHEET_ID).sheet1

def updatePaymentStatusInSheet(phone,status):
    try:
        # Filter data based on conditions
        data = worksheet.get_all_records()
        flag = False 
        for i, row in enumerate(data):
            if row["Phone number"] == phone:
                print(row)
                worksheet.update_cell(i+2, 16, status)
                print(f"Payment Status record updated for phone number: {phone}")
                flag = True
                break
        return flag

    except Exception as e:
        print(f"Error updating records: {e}")


