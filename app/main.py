from fastapi import FastAPI, Request, HTTPException,Form
from typing import Dict
import requests
from dotenv import load_dotenv
import os
from db import *
from utils import processWhatsAppMessage,processPayment
from fastapi.staticfiles import StaticFiles
from models import PaymentWebhookPayload
load_dotenv()


verify_token = os.getenv("VERIFY_TOKEN")

app = FastAPI()

app.mount("/template", StaticFiles(directory="./template"), name="template")
app.mount("/pdfs", StaticFiles(directory="./pdfs"), name="pdfs")


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(body)
    response = processWhatsAppMessage(body)
    return {"status": "ok"}

@app.post("/payment-webhook")
async def paymentWebhook(payload: Request):
    data = await payload.form()
    #result = processPayment(payload)
    return {"message": "Webhook received successfully"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    hub = request.query_params
    if hub["hub.mode"] == "subscribe" and hub["hub.verify_token"] == verify_token:
        return int(hub["hub.challenge"])
    else:
        raise HTTPException(status_code=403, detail="Invalid token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="77.37.44.233", port=8000)
