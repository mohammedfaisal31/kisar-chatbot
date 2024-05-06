from fastapi import APIRouter, FastAPI, Request, HTTPException, Form
from typing import Dict
import requests
from dotenv import load_dotenv
import os
from db import *
from utils import processWhatsAppMessage, processPayment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

verify_token = os.getenv("VERIFY_TOKEN")

# Create a router with prefix "/kisar"
kisar_router = APIRouter(prefix="/kisar")

# Define your FastAPI app
app = FastAPI()

# Mount static directories
app.mount("/kisar/template", StaticFiles(directory="./template"), name="template")
app.mount("/kisar/pdfs", StaticFiles(directory="./pdfs"), name="pdfs")

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

# Include the kisar_router in the main app
app.include_router(kisar_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
