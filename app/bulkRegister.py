import gspread
import os
from dotenv import load_dotenv
from userUtils import *
from db import get_db
import pandas as pd
import uuid
import zipfile
from io import BytesIO
from fastapi import FastAPI, HTTPException, Response
from qr import generate_pdf_with_qr_and_text
from models import User

# Load environment variables
load_dotenv()

# Replace with your sheet ID
SHEET_ID = os.getenv('SHEET_ID')


db = get_db()
# Authorize access to Google Sheets
gc = gspread.service_account(filename='./gcloud_cred.json')
worksheet = gc.open_by_key(SHEET_ID).worksheet("BULK")


def getPackageID(package_code):
    package_code_to_id = {
        'NR1-1': 1,
        'NR1-2': 2,
        'SO1-1': 3,
        'SO1-2': 4,
        'DO1-1': 5,
        'DO1-2': 6
    }

    # Return the package ID for the given package code
    return package_code_to_id.get(package_code, "Invalid package code")


async def bulkRegister():
    print("Reached")
    try:
        # Read the data from the sheet
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        print(data)
        # Create directories if not exists
        os.makedirs("./pdfs", exist_ok=True)
        os.makedirs("./pdfs", exist_ok=True)
        
        os.makedirs("./images", exist_ok=True)

        
        # Prepare a dictionary to hold ZIP files for each organization
        org_zip_buffers = {}
            
        
        for index, row in df.iterrows():
            if row['Pdf Status'] != 'GENERATED':
                org_pdf_path = ""
                if(row["Organisation"]):
                    org_pdf_path = f"./pdfs/{row['Organisation'].replace(' ','_')}/"
                    os.makedirs(org_pdf_path,exist_ok=True)
                # Generate unique payment ID
                payment_id = str(uuid.uuid4().hex)
                print(payment_id)
                # Create a new User object
                package_id = getPackageID(row['Select the package'])
                if not package_id:
                    package_id = 1
                new_user = User(
                    user_honorific=row['Honorific'],
                    user_first_name=row['First Name'],
                    user_middle_name=row['Middle Name'],
                    user_last_name=row['Last Name'],
                    user_email=row['Email'],
                    user_phone=row['Phone number'],
                    user_med_council_number=row['Medical Council Number'],
                    user_category=row['Category'],
                    user_type=row['Type Of Visitor'],
                    user_package_id=package_id,
                    user_city=row['City'],
                    user_state_of_practice=row['State'],
                    user_payment_id=payment_id,
                    user_payment_status='SUCCESS',
                    user_registration_type='DEFAULT',
                    user_organisation=row['Organisation']
                )

                db.add(new_user)
                db.commit()
                print("New user added")
                # Generate the PDF with QR code
                _template_path = ""
                if row['Category'] == "Faculty":
                    _template_path = "./template/faculty_500.png"
                else:
                    _template_path = "./template/delegate_500.png"
                
                generate_pdf_with_qr_and_text(
                    template_path=_template_path,  # Replace with your template path
                    pdf_path=org_pdf_path+payment_id+".pdf",
                    payment_id=payment_id,
                    honorific=row['Honorific'],
                    first_name=row['First Name'],
                    middle_name=row['Middle Name'],
                    last_name=row['Last Name'],
                    city=row['City'],
                    state=row['State']
                )

                # Organize PDFs into ZIP files based on the organization
                org_name = row['Organisation']
                if org_name not in org_zip_buffers:
                    org_zip_buffers[org_name] = BytesIO()
                
                with zipfile.ZipFile(org_zip_buffers[org_name], 'a') as zip_file:
                    zip_file.write(org_pdf_path, os.path.basename(org_pdf_path))

                # Update the sheet with PDF status
                worksheet.update_cell(index + 2, df.columns.get_loc("Pdf Status") + 1, "GENERATED")

        db.close()

        # Prepare multi-part response with ZIP files
        response = Response()
        response.headers['Content-Type'] = 'multipart/form-data; boundary=boundary'

        parts = []
        for org_name, zip_buffer in org_zip_buffers.items():
            zip_buffer.seek(0)
            part_headers = {
                'Content-Disposition': f'form-data; name="files"; filename="{org_name}.zip"',
                'Content-Type': 'application/zip'
            }
            part = {
                'headers': part_headers,
                'content': zip_buffer.getvalue()
            }
            parts.append(part)

        # Build the multi-part response
        multipart_response = build_multipart_response(parts)
        return Response(content=multipart_response, media_type='application/x-zip-compressed')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def build_multipart_response(parts):
    boundary = "boundary"
    multipart_body = ""

    for part in parts:
        multipart_body += f'--{boundary}\r\n'
        for key, value in part['headers'].items():
            multipart_body += f'{key}: {value}\r\n'
        multipart_body += '\r\n'
        multipart_body += part['content'].decode('latin1')
        multipart_body += '\r\n'

    multipart_body += f'--{boundary}--\r\n'
    return multipart_body
