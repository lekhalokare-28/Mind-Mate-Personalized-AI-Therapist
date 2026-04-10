!pip install -q -U google-genai


from google import genai

client = genai.Client(api_key="AIzaSyCuqJj1mPWDgffJJ93j50MVrQmyWnRMwqw")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)



import requests
import json
import speech_recognition as sr
from textblob import TextBlob
import threading
import time
import random
import datetime

# Gemini API Key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key

# Session Tracking
user_session = []
rewards = 0

# Function to get AI therapist response
def get_gemini_response(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_input}]}],
        "systemInstruction": {
            "role": "system",
            "parts": [{"text": "You are an AI therapist designed to provide mental health support."}]
        },
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500}
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            return response_data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "I'm sorry, I couldn't process that."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Sentiment Analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Speech-to-Text Function
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Speech recognition service unavailable."

# Gamification: Reward System
def update_rewards():
    global rewards
    rewards += 10
    print(f"You've earned 10 points! Total rewards: {rewards}")

# Progressive Tracking
def track_progress(user_message, sentiment):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_session.append({"timestamp": timestamp, "message": user_message, "sentiment": sentiment})
    print("Session updated!")

# Personalized Recommendations
def recommend_exercises(sentiment):
    recommendations = {
        "Positive": ["Try meditation", "Practice gratitude journaling", "Go for a nature walk"],
        "Neutral": ["Try deep breathing exercises", "Listen to calming music", "Read a book"],
        "Negative": ["Do a short workout", "Talk to a close friend", "Engage in creative activities"]
    }
    return random.choice(recommendations[sentiment])

# Daily AI Check-ins
def daily_check_in():
    while True:
        time.sleep(86400)  # Runs every 24 hours
        print("Daily AI Check-in: How are you feeling today?")
        user_message = input("You: ")
        sentiment = analyze_sentiment(user_message)
        response = get_gemini_response(user_message)
        track_progress(user_message, sentiment)
        print(f"\nAI Therapist: {response} (Sentiment: {sentiment})\n")

# Start Daily Check-ins as a Background Thread
check_in_thread = threading.Thread(target=daily_check_in, daemon=True)
check_in_thread.start()

# Main Chatbot Loop
if __name__ == "__main__":
    print("Hello! I'm your AI therapist. How can I assist you today?")
    
    while True:
        print("Would you like to speak or type? (say 'voice' for voice input, or type your message)")
        mode = input("Mode: ")
        
        if mode.lower() == "voice":
            user_message = voice_input()
        else:
            user_message = input("You: ")
        
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("AI Therapist: Take care! Goodbye!")
            break
        
        sentiment = analyze_sentiment(user_message)
        response = get_gemini_response(user_message)
        track_progress(user_message, sentiment)
        update_rewards()
        exercise_suggestion = recommend_exercises(sentiment)
        
        print(f"\nAI Therapist: {response} (Sentiment: {sentiment})\n")
        print(f"Based on your mood, I suggest: {exercise_suggestion}\n")
