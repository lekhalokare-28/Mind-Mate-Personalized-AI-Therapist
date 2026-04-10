#THIS FILES STORES THE CODE WHICH SENDS THE EMERGENY ALERT TO THE EMERGENCY CONTACT GIVEN BY THE USER 





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Dummy user database (Replace with actual database)
USER_DATA = {
    "USER_ID_HERE": {
        "name": "John Doe",
        "emergency_contact": "+1234567890"  # Replace with actual contact number
    }
}

class AlertRequest(BaseModel):
    userId: str

@app.post("/send_alert")
async def send_alert(request: AlertRequest):
    user = USER_DATA.get(request.userId)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    emergency_contact = user["emergency_contact"]
    user_name = user["name"]

    # Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = f"⚠️ URGENT: {user_name} activated the emergency alert in the AI Therapist app. Please check on them ASAP!"

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=emergency_contact
        )
        return {"status": "success", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send alert: {str(e)}")
