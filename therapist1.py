import google.generativeai as genai
import nltk
import random
import json
import os
from dotenv import load_dotenv
# Configure Gemini API key (Replace with your key)
load_dotenv("credentials.env")  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import requests
import keyboard  # For hotkey detection
import sys
import msvcrt  # Windows-specific nonblocking input
import time
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import speech_recognition as sr
import geocoder  # To detect user location
import torch


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json # LIBRARIES FOR EMERGENCY CONTACT FUNCTION

# Download necessary data for VADER
nltk.download("vader_lexicon")


# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Pre-trained Emotion Classifier (distill roBERT)
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)
# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# File to store user emotion history (if needed)
USER_MEMORY_FILE = "user_emotions.json"

# Function to load user emotion history
def load_user_memory():
    if os.path.exists(USER_MEMORY_FILE):
        with open(USER_MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save user emotion history
def save_user_memory(user_memory):
    with open(USER_MEMORY_FILE, "w") as file:
        json.dump(user_memory, file, indent=4)

# Function to track user emotions over time
def track_user_emotion(user_id, emotion):
    user_memory = load_user_memory()

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emotion": emotion
    })

    save_user_memory(user_memory)

# Function to summarize user emotions over the last sessions
def summarize_user_emotions(user_id):
    user_memory = load_user_memory()

    if user_id not in user_memory or len(user_memory[user_id]) == 0:
        return "No previous emotions tracked."

    last_emotions = user_memory[user_id][-5:]  # Get last 5 emotions
    emotions_summary = [entry["emotion"] for entry in last_emotions]
    most_common_emotion = max(set(emotions_summary), key=emotions_summary.count)

    return f"Recently, you've mostly been feeling '{most_common_emotion}'. How are you feeling today?"


# Global flag for voice mode (default OFF)
voice_mode = False

# Function to toggle voice mode using "Ctrl + 9"
def toggle_voice_mode():
    global voice_mode
    voice_mode = not voice_mode
    print("\n🔄 Voice Mode:", "ON" if voice_mode else "OFF")

# Register hotkey (runs in a separate thread)
keyboard.add_hotkey("ctrl+9", toggle_voice_mode)

# Windows-specific nonblocking text input function using msvcrt
def get_text_input(prompt="You: "):
    global voice_mode
    print(prompt, end="", flush=True)
    input_chars = []
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getwche()  # Read character and echo it
            # If Enter key is pressed, return the accumulated input
            if char in ("\r", "\n"):
                print("")  # Move to next line
                return "".join(input_chars).strip()
            # Handle backspace (ASCII 8)
            elif ord(char) == 8:
                if input_chars:
                    input_chars.pop()
                    sys.stdout.write("\b \b")
            else:
                input_chars.append(char)
        time.sleep(0.05)  # Delay to reduce CPU usage
        # If voice_mode is toggled while typing, immediately exit to voice mode
        if voice_mode:
            print("\n🔄 Switching to Voice Mode.")
            return None


# Mental Health Helplines by Country
helplines = {
    "US": "+1-800-273-8255 (National Suicide Prevention Lifeline)",
    "Canada": "+1-833-456-4566 (Talk Suicide Canada)",
    "India": "9152987821 (Vandrevala Foundation) | 1800-599-0019 (iCall)",
    "UK": "116 123 (Samaritans Helpline)",
    "Australia": "13 11 14 (Lifeline Australia)",
    "Germany": "0800-111-0111 (Telefonseelsorge)",
    "France": "3114 (National Suicide Prevention Helpline)",
    "Italy": "800-860-022 (Telefono Amico Italia)",
    "Spain": "024 (Suicide Prevention Helpline)",
    "Netherlands": "0800-0113 (113 Suicide Prevention)",
    "South Africa": "0800-567-567 (SADAG Mental Health Helpline)",
    "Brazil": "188 (CVV - Centro de Valorização da Vida)",
    "Mexico": "800-911-2000 (SAPTEL)",
    "Japan": "0570-064-556 (Inochi no Denwa)",
    "China": "400-161-9995 (Lifeline Shanghai, English Service)",
    "Singapore": "1800-221-4444 (Samaritans of Singapore - SOS)",
    "Philippines": "1553 (Mental Health Crisis Hotline)",
    "Malaysia": "03-2935-9935 (Befrienders KL)",
    "Indonesia": "119 (Indonesian Mental Health Helpline)",
    "New Zealand": "1737 (Need to Talk? Free Call or Text)",
    "Russia": "8-800-2000-122 (Psychological Help for Children & Adults)",
    "UAE": "800-4673 (Mental Support Line)",
    "Saudi Arabia": "920-033-360 (National Mental Health Centre)",
    "South Korea": "1393 (Suicide Prevention Helpline) | 1588-9191 (Mental Health Centre)",
    "Pakistan": "042-35761999 (Rozan Helpline) | 1122 (Emergency Helpline)",
    "Bangladesh": "0131-2300-603 (Kaan Pete Roi Helpline)",
    "Thailand": "1323 (Mental Health Hotline)",
    "Vietnam": "1900-6233 (Free Psychological Support Hotline)",
    "Egypt": "0800-888-0700 (Mental Health Helpline)",
    "Nigeria": "0800-800-2000 (Mental Health Foundation Nigeria)",
    "Argentina": "135 (Centro de Asistencia al Suicida - CAS)",
    "Chile": "600-360-7777 (Salud Responde Mental Health Line)",
    "Colombia": "106 (Mental Health Helpline)",
}


# Function to get user's location
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        country = data.get("country", "Unknown")
        city = data.get("city", "Unknown")
        return country, city
    except requests.RequestException:
        return "Unknown", "Unknown"

# Function to get the localized helpline
def get_helpline():
    country, _ = get_user_location()
    return helplines.get(country)

print(get_helpline())  

# Function to recognize speech with confirmation
import speech_recognition as sr

def recognize_speech():
    global voice_mode  # Ensure we modify the global voice_mode variable
    recognizer = sr.Recognizer()
    no_input_attempts = 0  # Counter for handling no input cases

    while no_input_attempts < 2:  # Allow up to 2 failed attempts
        with sr.Microphone() as source:
            print("🎤 Listening... Speak now.")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
                text = recognizer.recognize_google(audio)
                print(f"📢 You said: {text}")

                # Ask user to confirm, retry, or cancel
                while True:
                    confirm = input("✔️ Confirm (Y) | 🔄 Retry (R) | ❌ Cancel Voice (E): ").strip().lower()
                    if confirm == "y":
                        return text  # Return recognized speech
                    elif confirm == "r":
                        print("🔄 Retrying...")
                        break  # Exit inner loop and retry listening
                    elif confirm == "e":
                        print("❌ Switching to text mode.")
                        voice_mode = False  # <-- TURN OFF VOICE MODE
                        return None  # Immediately return to exit both loops
                    else:
                        print("⚠️ Invalid input. Please enter Y, R, or E.")
                        continue  # Ask for input again
            
            except sr.UnknownValueError:
                no_input_attempts += 1
                print(f"❌ No voice detected. Attempt {no_input_attempts}/2. Please speak.")
            except sr.RequestError:
                print("⚠️ Could not request results. Check your connection.")
                return None  # Exit completely if API request fails
            except KeyboardInterrupt:
                print("\n🚪 Exiting speech recognition.")
                return None  # Gracefully exit on Ctrl+C 

    # After 2 failed attempts, switch to text mode
    print("❌ No input received. Switching to text mode.")
    voice_mode = False
    return None

# Function to analyze sentiment and emotion
def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    polarity = sentiment_scores['compound']
    emotion_scores = emotion_classifier(text)
    sentiment = "positive" if polarity > 0.05 else "negative" if polarity < -0.05 else "neutral"
    if isinstance(emotion_scores, list) and len(emotion_scores) > 0:
        predicted_emotion = max(emotion_scores, key=lambda x: x['score'])['label']
        emotion_confidence = round(max(emotion_scores, key=lambda x: x['score'])['score'] * 100, 2)
    else:
        predicted_emotion = "unknown"
        emotion_confidence = 0.0
        # If the text has both positive and negative keywords, prioritize negative sentiment
        # Step 3: Context-aware adjustments
    negative_keywords = ["die", "suicide", "kill", "hopeless", "depressed", "suffer"]
    positive_keywords = ["love", "happy", "joy", "hahaha", "fun"]
    if any(word in text.lower() for word in negative_keywords) and any(word in text.lower() for word in positive_keywords):
        sentiment = "negative"
        predicted_emotion = "sadness"
        emotion_confidence = max(emotion_confidence, 90)  # Increase confidence in extreme cases

    return {
        "sentiment": sentiment,
        "emotion": predicted_emotion,
        "sentiment_score": polarity,
        "emotion_confidence": emotion_confidence
    }

# Function to get AI response from Gemini via REST API call and to store conversation history (for memory)

chat_history = []

def get_gemini_response(user_input):
    global chat_history

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    # Append user's latest message to history
    chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Limit history length to avoid excessive context (adjust as needed)
    if len(chat_history) > 10:  # Keeps last 10 exchanges
        chat_history = chat_history[-10:]

    # Construct API payload with full conversation memory
    country, city = get_user_location()
    payload = {
        "contents": chat_history,  # Send entire conversation history
        "systemInstruction": {
            "role": "system",
            "parts": [{"text": 
                "You are an AI therapist providing mental health support. "
                "Ensure responses are **concise (~100 words)** yet helpful. "
                "Follow this structure: "
                "Acknowledge feelings in one sentence. "
                "Provide 1-2 practical tips briefly. "
                "End with encouragement or a gentle follow-up question. "
                "Keep responses **cohesive** with previous conversation history and avoid repetition."
                f"You are an AI therapist providing mental health support. "
                f"The user is in {city}, {country}. Provide helplines and guidance relevant to this location."
            }]
        },
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 150
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        try:
            ai_response = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()

            # Append AI's response to history
            chat_history.append({"role": "model", "parts": [{"text": ai_response}]})

            return ai_response
        except (KeyError, IndexError):
            return "I'm sorry, I couldn't process that. How else can I support you?"
    else:
        return f"Error: {response.status_code} - {response.text}"




# Main chatbot function
def chatbot():
    global voice_mode
    user_id = input("Enter your username: ")
    print("Hello! I'm your AI therapist. How can I assist you today?")
    print(summarize_user_emotions(user_id))  # Show emotional trends
    while True:
        # Use voice input if voice_mode is active; otherwise, use text input.
        if voice_mode:
            user_message = recognize_speech()
            # If voice input was canceled, fallback to text input.
            
        else:
            user_message = get_text_input("You: ")
        
        if user_message is None:
            continue  # Restart loop if no valid message is received
        
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("AI Therapist: Take care! Goodbye! 👋")
            break 
        
        # Analyze sentiment and emotion
        analysis_result = analyze_sentiment(user_message)
        sentiment = analysis_result["sentiment"]
        emotion = analysis_result["emotion"]
        confidence = analysis_result["emotion_confidence"]
        print(f"🔍 Detected Mood: {emotion} (Confidence: {confidence}%)")
        print(f"📊 Sentiment Analysis: {sentiment}")


        # Track user emotions
        track_user_emotion(user_id, emotion)
        
        # Get AI response from Gemini
        ai_response = get_gemini_response(user_message)
        
        # Optionally adjust the AI response based on sentiment/emotion
        if sentiment == "negative":
            ai_response += "\n\n💡 Remember, you are not alone. Take a deep breath, and let’s talk about it."
        elif emotion == "overwhelmed":
            ai_response += "\n\n🌿 It sounds like you're feeling overwhelmed. Have you tried taking a short break or practicing mindfulness?"
        elif emotion == "grateful":
            ai_response += "\n\n😊 I'm glad to hear that! Keep embracing the good moments!"
        
        print(f"\n🤖 AI Therapist: {ai_response}\n")

        

if __name__ == "__main__":
    chatbot()







# FUNCTION FOR STORING EMERGENCY CONTACT DETAILS 

app = FastAPI()

JSON_FILE = "users.json"

# Function to load user data from JSON
def load_users():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

# Function to save user data to JSON
def save_users(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

# User Signup Model
class UserSignup(BaseModel):
    id: str
    name: str
    email: str
    password: str  # Password should be hashed in production!
    emergency_contact: str

# Panic Alert Request Model
class AlertRequest(BaseModel):
    userId: str

@app.post("/signup")
def signup(user: UserSignup):
    users = load_users()
    
    # Check if email already exists
    if any(u["email"] == user.email for u in users["users"]):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,  # Hash passwords in production
        "emergency_contact": user.emergency_contact
    }
    
    users["users"].append(new_user)
    save_users(users)
    
    return {"message": "User registered successfully"}

@app.post("/send_alert")
def send_alert(request: AlertRequest):
    users = load_users()

    # Find user
    user = next((u for u in users["users"] if u["id"] == request.userId), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    emergency_contact = user["emergency_contact"]
    user_name = user["name"]

    # Here, you can integrate Twilio or any SMS service
    message_body = f"⚠️ URGENT: {user_name} activated the emergency alert in AI Therapist. Please check on them!"

    # Simulating SMS sending (replace this with Twilio)
    print(f"Sending SMS to {emergency_contact}: {message_body}")

    return {"status": "success", "message": "Alert sent successfully"}





#FUNCTION TO STORE THE DATA FEOM THE MOOD SCALE FROM THE JOURNAL PAGE 

app = FastAPI()
MOOD_DATA_FILE = "mood_data.json"

# Load mood data
def load_mood_data():
    try:
        with open(MOOD_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"moods": []}

# Save mood data
def save_mood_data(data):
    with open(MOOD_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Mood Rating Model
class MoodEntry(BaseModel):
    userId: str
    mood: int
    timestamp: str

@app.post("/submit_mood")
def submit_mood(entry: MoodEntry):
    data = load_mood_data()

    # Add new mood entry
    new_entry = {
        "userId": entry.userId,
        "mood": entry.mood,
        "timestamp": entry.timestamp
    }
    data["moods"].append(new_entry)
    save_mood_data(data)

    return {"message": "Mood data saved successfully"}

@app.get("/weekly_mood/{userId}")
def get_weekly_mood(userId: str):
    data = load_mood_data()
    today = datetime.utcnow()
    one_week_ago = today - timedelta(days=7)

    user_moods = [entry for entry in data["moods"] if entry["userId"] == userId]
    
    weekly_moods = [
        {"date": entry["timestamp"], "mood": entry["mood"]}
        for entry in user_moods
        if datetime.fromisoformat(entry["timestamp"]) >= one_week_ago
    ]

    return {"weekly_mood": weekly_moods}





