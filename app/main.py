from fastapi import FastAPI, Request, HTTPException
import requests
from dotenv import load_dotenv
import os
from utils import processWhatsAppMessage

load_dotenv()


verify_token = os.getenv("VERIFY_TOKEN")

app = FastAPI()



@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    response = processWhatsAppMessage(body)
    return {"status": "ok"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    hub = request.query_params
    if hub["hub.mode"] == "subscribe" and hub["hub.verify_token"] == verify_token:
        return int(hub["hub.challenge"])
    else:
        raise HTTPException(status_code=403, detail="Invalid token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
