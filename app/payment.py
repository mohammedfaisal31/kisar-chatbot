from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("INSTAMOJO_KEY")
AUTH_TOKEN=os.getenv("INSTAMOJO_AUTH_TOKEN")
HOST=os.getenv("HOST")
ENV=os.getenv("ENVIRONMENT")
from instamojo_wrapper import Instamojo


#Production
api = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN)

#Sanbox
if ENV == "dev":
    api = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')

def createPaymentLink(paymentDetails):
    response = api.payment_request_create(
        amount=paymentDetails["amount"],
        purpose=paymentDetails["purpose"],
        send_email=True,
        buyer_name=paymentDetails["buyer_name"],
        phone=paymentDetails["phone"],
        email=paymentDetails["email"],
        redirect_url=f"{HOST}/payment-success",
        webhook=f"{HOST}/payment-webhook"
    )
    print(response)
    return response