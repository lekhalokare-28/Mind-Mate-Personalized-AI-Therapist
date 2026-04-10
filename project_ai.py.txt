!pip install -q -U google-genai
!pip install SpeechRecognition pyaudio
import speech_recognition as sr

from google import genai

client = genai.Client(api_key="AIzaSyCuqJj1mPWDgffJJ93j50MVrQmyWnRMwqw")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)

import requests
import json
from textblob import TextBlob


GEMINI_API_KEY = "AIzaSyCuqJj1mPWDgffJJ93j50MVrQmyWnRMwqw"  # Replace with your actual API key



def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Could not request results."

user_input = recognize_speech()
print("User said:", user_input)

def get_gemini_response(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyA1eDF9DcqJCT5KGeXBBXx06PKsGgfvKUU"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": user_input}
                ]
            }
        ],
        "systemInstruction": {
            "role": "system",
            "parts": [
                {"text": "You are an AI therapist designed to provide mental health support."}
            ]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
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

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    print("Hello! I'm your AI therapist. How can I assist you today?")

    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("AI Therapist: Take care! Goodbye!")
            break

        sentiment = analyze_sentiment(user_message)
        response = get_gemini_response(user_message)
        print(f"AI Therapist: {response} (Sentiment: {sentiment})")
