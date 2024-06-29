from fastapi import APIRouter, FastAPI, Request, HTTPException, Form
from typing import Dict
import requests
from dotenv import load_dotenv
import os
from db import *
from models import *
from utils import processWhatsAppMessage, processPayment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import uuid
from utils import * 
from bulkRegister import bulkRegister
from io import BytesIO
import zipfile
from qr import * 
import tempfile


load_dotenv()

verify_token = os.getenv("VERIFY_TOKEN")

# Create a router with prefix "/kisar"
kisar_router = APIRouter(prefix="/kisar")

# Define your FastAPI app
app = FastAPI()

# Mount static directories
app.mount("/kisar/template", StaticFiles(directory="./template"), name="template")
app.mount("/kisar/pdfs", StaticFiles(directory="./pdfs"), name="pdfs")
app.mount("/kisar/badges", StaticFiles(directory="./badges"), name="badges")


# Endpoint for /kisar/webhook
@kisar_router.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(body)
    response = processWhatsAppMessage(body)
    return {"status": "ok"}

# Endpoint for /kisar/payment-webhook
@kisar_router.post("/payment-webhook")
async def paymentWebhook(payload: Request):
    data = await payload.form()
    # print(data["amount"])
    result = processPayment(data)
    return {"message": "Webhook received successfully"}

# Endpoint for /kisar/payment-success
@kisar_router.get("/payment-success")
async def paymentSuccess():
    return FileResponse("paymentSuccess.html")

# Endpoint for verification of webhook
@kisar_router.get("/webhook")
async def verify_webhook(request: Request):
    hub = request.query_params
    if hub["hub.mode"] == "subscribe" and hub["hub.verify_token"] == verify_token:
        return int(hub["hub.challenge"])
    else:
        raise HTTPException(status_code=403, detail="Invalid token")

@kisar_router.get("/bulk-register")
async def process_data():
    return await bulkRegister()

# New endpoint for sending badge
@kisar_router.post("/send-badge")
async def send_badge(request: Request):
    db = get_db()
    body = await request.json()
    user_payment_id: Optional[str] = body.get("user_payment_id")
    user_phone: Optional[str] = body.get("user_phone")
    
    if not user_payment_id and not user_phone:
        raise HTTPException(status_code=400, detail="Either user_payment_id or user_phone must be provided.")

    if user_phone:
        user = db.query(User).filter(User.user_phone == user_phone).first()
        template_path=''
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if user.user_payment_id == "MOJO":
            if user.user_category == "Delegate":
                template_path = "./template/delegate_500.png"
            else:
                template_path = "./template/faculty_500.png"

            
            user_payment_id = str(uuid.uuid4())
            user.user_payment_id = user_payment_id
            pdf_path=f"./pdfs/{user_payment_id}.pdf"
            generate_pdf_with_qr_and_text(
            template_path, pdf_path, user.user_payment_id, user.user_honorific, user.user_first_name,
            user.user_middle_name, user.user_last_name, user.user_city, user.user_state_of_practice
            )
            db.commit()
        else:
            user_payment_id = user.user_payment_id
        sendDocumentTemplate('91'+user.user_phone, user.user_payment_id)

    elif user_payment_id:
        user = db.query(User).filter(User.user_payment_id == user_payment_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        sendDocumentTemplate('91'+user.user_phone, user.user_payment_id)

@kisar_router.get("/generate_badges/")
async def generate_badges():
    db = get_db()
    payment_ids: list[str] = ["MOJO4629X05Q28349079"]
    
    if not payment_ids:
        raise HTTPException(status_code=400, detail="Payment IDs list is empty.")

    output_dir = "./badges/"
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for payment_id in payment_ids:
                user = db.query(User).filter(User.user_payment_id == payment_id).first()
                if not user:
                    continue
                template_path = "./template/delegate_cut_500.png" if user.user_category == "Delegate" else "./template/faculty_cut_500.png"
                output_image_path = os.path.join(output_dir, f"{payment_id}.png")
                if generate_badge_with_qr_and_text(
                    template_path,
                    output_image_path,
                    user.user_payment_id,
                    user.user_honorific,
                    user.user_first_name,
                    user.user_middle_name,
                    user.user_last_name,
                    user.user_city,
                    user.user_state_of_practice,
                ):
                    zf.write(output_image_path, f"{payment_id}.png")

    return FileResponse(
        tmp_file.name,
        media_type="application/x-zip-compressed",
        filename="badges.zip"
    )

# Include the kisar_router in the main app
app.include_router(kisar_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

