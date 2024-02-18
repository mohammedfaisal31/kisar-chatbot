# main.py
from fastapi import FastAPI
from whatsapp import *

app = FastAPI()

@app.post("/webhook")
async def webhook():
    return await handle_webhook()

@app.get("/test")
async def hello():
    body = { 
        "messaging_product": "whatsapp", 
        "to": "917204847042",
        "type": "template", 
        "template": 
            { 
                "name": "isar_event_registration_link",
                "language": 
            { 
                "code": "en" 
          
            }
        } 
  
    }
    return await call_whatsapp_api("https://graph.facebook.com/v18.0/202554606283438/messages","EAAKNYZACUTs0BO396mWfFIKFI3pwP33G00SdmTDxN04Amhl6PWsfZCer2ZBm7IK0fyvhfdm2VU2Gd8O5C2z9DfD2968BEkndXVk8VMb4H1Oiz9WHeGeugAk3qI6DhJbKTHhKn7NySSf1trepKMxeRCqzZAv1kehxEfXO6T3zjAorAKhmprwy38wCcQtSIOQsx09HaIZA96x41ZCJYIltsY",body)

@app.post("/register")
async def register_for_event(event_name: str):
    return await register_for_event(event_name)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
