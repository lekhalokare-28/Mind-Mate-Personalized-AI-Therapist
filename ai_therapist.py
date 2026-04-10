import google.generativeai as genai
import nltk
import random
import json
import os
import requests
import keyboard  # ✅ Hotkey for voice toggle
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import speech_recognition as sr

# Download necessary data for VADER
nltk.download("vader_lexicon")

# Load Pre-trained Emotion Classifier (BERT)
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", return_all_scores=True)

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# File to store user emotion history
USER_MEMORY_FILE = "user_emotions.json"

# ✅ Global variable for voice mode toggle
voice_mode = False  

# Function to toggle voice mode using "Ctrl + 9"
def toggle_voice_mode():
    global voice_mode
    voice_mode = not voice_mode  # Toggle between True and False
    print("\n🔄 Voice Mode:", "ON" if voice_mode else "OFF")

# ✅ Listen for "Ctrl + 9" hotkey
keyboard.add_hotkey("ctrl+9", toggle_voice_mode)

# Function to recognize speech with confirmation
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now.")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"📢 You said: {text}")

            # ✅ Ask user to confirm or retry
            while True:
                confirm = input("✔️ Confirm (Y) | 🔄 Retry (R) | ❌ Exit voice (E): ").strip().lower()
                
                if confirm == "y":
                    return text  # Send text to AI
                elif confirm == "r":
                    print("🔄 Retrying...")
                    return recognize_speech()  # Retry speech input
                elif confirm == "e":
                    print("❌ Switching to text mode.")
                    return None  # Stop voice mode

        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand. Try again.")
            return recognize_speech()  # Retry if unrecognized
        except sr.RequestError:
            print("⚠️ Could not request results. Check your connection.")
            return None

# Function to analyze sentiment and emotion
def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    polarity = sentiment_scores['compound']
    emotion_scores = emotion_classifier(text)[0]
    predicted_emotion = max(emotion_scores, key=lambda x: x['score'])['label']
    emotion_confidence = round(max(emotion_scores, key=lambda x: x['score'])['score'] * 100, 2)

    sentiment = "positive" if polarity > 0.05 else "negative" if polarity < -0.05 else "neutral"

    return {
        "sentiment": sentiment,
        "emotion": predicted_emotion,
        "sentiment_score": polarity,
        "emotion_confidence": emotion_confidence
    }

# Function to get AI response from Gemini
def get_gemini_response(user_input):
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyA1eDF9DcqJCT5KGeXBBXx06PKsGgfvKUU"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": user_input}]}
        ],
        "systemInstruction": {
            "role": "system",
            "parts": [{"text": "You are an AI therapist providing mental health support."}]
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

# ✅ Main Chatbot Function
def chatbot():
    global voice_mode  # Use global voice_mode variable

    user_id = input("Enter your username: ")  # Unique ID to track user emotions
    print("Hello! I'm your AI therapist. How can I assist you today?")
    
    while True:
        # 🔄 Check if voice mode is ON or OFF dynamically
        if voice_mode:
            user_message = recognize_speech()
            if user_message is None:
                continue  # Skip if voice input was canceled
        else:
            user_message = input("You: ").strip()

        # ✅ Exit condition
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("AI Therapist: Take care! Goodbye! 👋")
            break

        # ✅ Analyze sentiment & emotion
        analysis_result = analyze_sentiment(user_message)
        sentiment = analysis_result["sentiment"]
        emotion = analysis_result["emotion"]
        confidence = analysis_result["emotion_confidence"]

        print(f"🔍 Detected Mood: {emotion} (Confidence: {confidence}%)")
        print(f"📊 Sentiment Analysis: {sentiment}")

        # ✅ Get AI response from Gemini
        ai_response = get_gemini_response(user_message)

        # ✅ Modify response based on detected emotions
        if sentiment == "negative":
            ai_response += "\n\n💡 Remember, you are not alone. Take a deep breath, and let’s talk about it."
        elif emotion == "overwhelmed":
            ai_response += "\n\n🌿 It sounds like you're feeling overwhelmed. Have you tried taking a short break or practicing mindfulness?"
        elif emotion == "grateful":
            ai_response += "\n\n😊 I'm glad to hear that! Gratitude is a wonderful feeling. Keep embracing the good moments!"

        print(f"\n🤖 AI Therapist: {ai_response}\n")

if __name__ == "__main__":
    chatbot()
    