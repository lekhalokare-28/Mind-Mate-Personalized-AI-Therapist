from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Dummy sentiment analysis function (replace with actual logic)
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

# Dummy Gemini response function (replace with actual AI logic)
chat_history = []

def get_gemini_response(user_input):
    global chat_history

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyA1eDF9DcqJCT5KGeXBBXx06PKsGgfvKUU"
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


@app.post("/api/chat")
async def chat(request: ChatRequest):
    user_id = request.user_id
    user_message = request.message

    # Analyze sentiment and emotion
    analysis_result = analyze_sentiment(user_message)
    sentiment = analysis_result["sentiment"]
    emotion = analysis_result["emotion"]
    confidence = analysis_result["emotion_confidence"]

    # Generate AI response
    ai_response = get_gemini_response(user_message)

    # Adjust response based on emotion/sentiment
    if sentiment == "negative":
        ai_response += "\n\n💡 Remember, you are not alone. Take a deep breath, and let’s talk about it."
    elif emotion == "overwhelmed":
        ai_response += "\n\n🌿 It sounds like you're feeling overwhelmed. Have you tried taking a short break or practicing mindfulness?"
    elif emotion == "grateful":
        ai_response += "\n\n😊 I'm glad to hear that! Keep embracing the good moments!"

    # Return response
    return {
        "user_id": user_id,
        "response": ai_response,
        "detected_mood": emotion,
        "confidence": confidence,
    }

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)

