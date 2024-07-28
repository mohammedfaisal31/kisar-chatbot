from fastapi import APIRouter, FastAPI, Request, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from typing import Optional
import os
from dotenv import load_dotenv
from db import *
from models import *
from utils import processWhatsAppMessage, sendPaymentLinkTemplate, processPayment, generate_pdf_with_qr_and_text,sendDocumentTemplate
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bulkRegister import bulkRegister
from io import BytesIO
import zipfile
from qr import *
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from enum import Enum
import tempfile
import uuid


load_dotenv()

verify_token = os.getenv("VERIFY_TOKEN")

# Create a router with prefix "/kisar"
kisar_router = APIRouter(prefix="/kisar")

# Define your FastAPI app
app = FastAPI()

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CORS from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static directories
app.mount("/kisar/template", StaticFiles(directory="./template"), name="template")
app.mount("/kisar/pdfs", StaticFiles(directory="./pdfs"), name="pdfs")
app.mount("/kisar/badges", StaticFiles(directory="./badges"), name="badges")


class StateEnum(str, Enum):
    Karnataka = "Karnataka"
    Tamil_Nadu = "Tamil Nadu"
    Andhra_Pradesh = "Andhra Pradesh"
    Telangana = "Telangana"
    Kerala = "Kerala"
    Maharashtra = "Maharashtra"
    # Add other Indian states here
    # Example: Gujarat = "Gujarat", West_Bengal = "West Bengal", etc.
    # For brevity, add all other states as needed
    Gujarat = "Gujarat"
    West_Bengal = "West Bengal"
    Uttar_Pradesh = "Uttar Pradesh"
    Rajasthan = "Rajasthan"
    Punjab = "Punjab"
    Haryana = "Haryana"
    Himachal_Pradesh = "Himachal Pradesh"
    Uttarakhand = "Uttarakhand"
    Jammu_and_Kashmir = "Jammu and Kashmir"
    Ladakh = "Ladakh"
    Sikkim = "Sikkim"
    Arunachal_Pradesh = "Arunachal Pradesh"
    Nagaland = "Nagaland"
    Manipur = "Manipur"
    Mizoram = "Mizoram"
    Tripura = "Tripura"
    Assam = "Assam"
    Meghalaya = "Meghalaya"
    Andaman_and_Nicobar_Islands = "Andaman and Nicobar Islands"
    Chandigarh = "Chandigarh"
    Dadra_and_Nagar_Haveli = "Dadra and Nagar Haveli"
    Daman_and_Diu = "Daman and Diu"
    Delhi = "Delhi"
    Puducherry = "Puducherry"

class CertificateRequest(BaseModel):
    name: str
    medical_council_number: str
    state_of_medical_council: StateEnum
    category: str

@kisar_router.post("/generate_certificate")
async def generate_certificate(request: CertificateRequest):
    # Validate that medical_council_number contains only digits
    if not request.medical_council_number.isdigit():
        raise HTTPException(status_code=400, detail="Medical council number must contain only digits")

    # Prepare certificate text
    text_lines = [
        request.name,
        request.medical_council_number,
        request.state_of_medical_council
    ]

    # Choose template based on category
    if request.category.lower() == 'faculty':
        template_path = './certificate/faculty_certificate.png'
    elif request.category.lower() == 'delegate':
        template_path = './certificate/delegate_certificate.png'
    else:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Prepare output path
    output = BytesIO()
    
    # Overlay text on image
    overlay_text_on_png(template_path, output, text_lines, positions=[(730, 460), (302, 420), (230, 212)], font_path='./Courier-Bold.otf', font_size=30)

    # Create PDF from image
    pdf_path = "/tmp/certificate.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage(output, 0, 0, width=letter[0], height=letter[1])
    c.save()

    # Return PDF file as streaming response
    pdf_stream = open(pdf_path, "rb")
    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=certificate.pdf"})

@kisar_router.get("/certificate")
async def form():
    html = """
    <html>
    <head>
        <title>Certificate Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            h1 {
                color: #333;
                text-align: center;
                padding-top: 20px;
            }
            form {
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            label {
                font-weight: bold;
                display: block;
                margin: 10px 0 5px;
            }
            input, select {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #0867ec;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 4px;
            }
            input[type="submit"]:hover {
                background-color: #065bb5;
            }
        </style>
    </head>
    <body>
        <h1>Generate Certificate</h1>
        <form action="/generate_certificate" method="post">
            <label for="name">Name required in certificate:</label>
            <input type="text" id="name" name="name" required><br>
            
            <label for="medical_council_number">Medical council number (only digits):</label>
            <input type="text" id="medical_council_number" name="medical_council_number" pattern="\d+" required><br>
            
            <label for="state">State of Medical Council:</label>
            <select id="state" name="state" required>
                <option value="" disabled selected>Select your state</option>
                {state_options}
            </select><br>
            
            <label for="role">Role:</label>
            <select id="role" name="role" required>
                <option value="Faculty">Faculty</option>
                <option value="Delegate">Delegate</option>
            </select><br>
            
            <input type="submit" value="Generate Certificate">
        </form>
    </body>
    </html>
    """
    
    # Generate dropdown options from StateEnum
    state_options = "".join([f"<option value='{state}'>{state}</option>" for state in StateEnum])
    return html.format(state_options=state_options)

def overlay_text_on_png(template_path, output_path, text_lines, positions, font_path='./Courier-Bold.otf', font_size=20):
    # Load the template image
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    
    # Load a custom font
    font = ImageFont.truetype(font_path, font_size)
    
    # Draw each line of text
    for text, (x, y) in zip(text_lines, positions):
        draw.text((x, y), text, font=font, fill='black')  # Draw text on image
    
    # Save the modified image
    img.save(output_path)
# Include the kisar_router in the main app
app.include_router(kisar_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

