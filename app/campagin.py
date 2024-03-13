import gspread
import os
from dotenv import load_dotenv
import schedule
import time
from userUtils import *
from db import get_db
from utils import sendRegisterTemplate
import sys
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Replace with your sheet ID
SHEET_ID = os.getenv('CAMPAIGN_SHEET_ID')



# Authorize access to Google Sheets
gc = gspread.service_account(filename='./gcloud_cred.json')

def sendCampaignToState(state):
    try:
        worksheet = gc.open_by_key(SHEET_ID)
        sub_sheet = worksheet.worksheet(state)
        
        # Filter data based on conditions
        data = sub_sheet.get_all_records()
        progress_bar = tqdm(total=len(data), desc="Processing items")
        for i, row in enumerate(data):
            if len(str(row["Mobile1"])) == 10:
                sendRegisterTemplate("91"+str(row["Mobile1"]))
                shoot = 0
                if row["messages_sent"] != "":
                    shoot = row["messages_sent"] + 1
                sub_sheet.update_cell(i+2,6,shoot)
            if len(str(row["Mobile2"])) == 10:
                sendRegisterTemplate("91"+str(row["Mobile2"]))
                shoot = 0
                if row["messages_sent"] != "":
                    shoot = row["messages_sent"] + 1
                sub_sheet.update_cell(i+2,6,shoot)
            if len(str(row["Mobile3"])) == 10:
                sendRegisterTemplate("91"+str(row["Mobile3"]))
                shoot = 0
                if row["messages_sent"] != "":
                    shoot = row["messages_sent"] + 1
                sub_sheet.update_cell(i+2,6,shoot)
            progress_bar.update(1)
        progress_bar.close()
            
    except Exception as e:
        print(f"Error updating records: {e}")

if __name__ == "__main__":
    state = sys.argv[1]
    sendCampaignToState(state)
