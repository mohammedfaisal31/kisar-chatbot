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
from reportlab.lib.pagesizes import A4
import zipfile
from qr import *
from fastapi.responses import StreamingResponse,HTMLResponse
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
async def generate_certificate(
    name: str = Form(...),
    medical_council_number: str = Form(...),
    state_of_medical_council: StateEnum = Form(...),
    category: str = Form(...),
):
    # Validate that medical_council_number contains only digits
    if not medical_council_number.isdigit():
        raise HTTPException(status_code=400, detail="Medical council number must contain only digits")

    # Prepare certificate text
    text_lines = [
        name,
        medical_council_number,
        state_of_medical_council
    ]

    # Choose template based on category
    if category.lower() == 'faculty':
        template_path = './certificate/faculty_certificate.png'
    elif category.lower() == 'delegate':
        template_path = './certificate/delegate_certificate.png'
    else:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Prepare output path
    output = BytesIO()
    
    # Overlay text on image
    overlay_text_on_png(template_path, "./tmp/image.png", text_lines, positions=[(730, 460), (302, 420), (230, 212)], font_path='./Courier-Bold.otf', font_size=30)

    # Create PDF from image
    pdf_path = "./tmp/certificate.pdf"

    img = Image.open("./tmp/image.png")
    img_width, img_height = img.size

    # Calculate the aspect ratio
    aspect = img_width / img_height

    # Calculate new dimensions to fit A4 while maintaining aspect ratio
    a4_width, a4_height = A4
    if a4_width / a4_height > aspect:
        new_height = a4_height
        new_width = a4_height * aspect
    else:
        new_width = a4_width
        new_height = a4_width / aspect

    # Center the image on the PDF
    x_offset = (a4_width - new_width) / 2
    y_offset = (a4_height - new_height) / 2

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage("./tmp/image.png", x_offset, y_offset, width=new_width, height=new_height)
    c.save()
    
    # Return PDF file as streaming response
    pdf_stream = open(pdf_path, "rb")
    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=certificate.pdf"})

@kisar_router.get("/certificate")
async def form():
        # Generate state options HTML
    state_options = "\n".join(
        [f'<option value="{state}">{state}</option>' for state in StateEnum]
    )

    # HTML form template
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Certificate Form</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            form {{
                max-width: 600px;
                margin: 0 auto;
            }}
            label {{
                display: block;
                margin: 10px 0 5px;
            }}
            input, select {{
                width: 100%;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <h2>Generate Certificate</h2>
        <form action="/kisar/generate_certificate" method="post">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" required>

            <label for="medical_council_number">Medical Council Number</label>
            <input type="text" id="medical_council_number" name="medical_council_number" pattern="\d+" required>

            <label for="state_of_medical_council">State of Medical Council</label>
            <select id="state_of_medical_council" name="state_of_medical_council" required>
                {state_options}
            </select>

            <label for="category">Category</label>
            <select id="category" name="category" required>
                <option value="faculty">Faculty</option>
                <option value="delegate">Delegate</option>
            </select>

            <button type="submit">Generate Certificate</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

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

