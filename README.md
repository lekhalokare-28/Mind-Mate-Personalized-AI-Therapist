# 🧠 MindMate - Personalized AI Therapist

> An AI-powered mental health companion that listens, understands, and supports you — while knowing when to connect you with real help.

---

## 💡 About the Project

MindMate is a personalized AI therapist chatbot built to provide emotional support through intelligent conversation. It detects your mood, remembers your history, suggests mindfulness exercises, and escalates to emergency services when needed — all in a compassionate, user-friendly interface.

This project was built as part of my BCA (Data Science) program at SRM Institute of Science and Technology, Chennai.

---

## ✨ Features

- 🗣️ **Natural Conversation** — Powered by Google Gemini API for empathetic, context-aware responses
- 😊 **Advanced Emotion Detection** — Detects joy, sadness, fear, anger, sarcasm, gratitude, and more using VADER + DistilRoBERTa (BERT)
- 🎙️ **Voice & Text Input** — Users can switch between typing and speaking at any time
- 📍 **Location-Based Helplines** — Automatically suggests emergency helpline numbers based on the user's IP location
- 🧘 **Mindfulness Exercises** — Recommends breathing and grounding exercises (e.g. 5-4-3-2-1 method) based on detected mood
- 🧠 **Conversation Memory** — Remembers past sessions and greets users with emotional context ("Recently, you've mostly been feeling 'fear'. How are you feeling today?")
- 📓 **Journaling & Mood Tracking** — Users can write unlimited journal entries, log their mood on a 1–10 scale, and all mood data is automatically synced to the weekly mood analysis dashboard
- 📊 **Weekly Mood Visualization** — Interactive dashboard displaying weekly mood trends based on journal entries
- 🚨 **Panic Button** — Sends an SMS alert to the user's emergency contact via Twilio in crisis situations
- 🌐 **Multilingual Support** — Powered by Gemini's native multilingual capabilities, MindMate can converse in multiple languages including Hindi

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI / Conversation | Google Gemini API |
| Sentiment Analysis | VADER (NLTK), DistilRoBERTa (Hugging Face Transformers) |
| Backend | Python, FastAPI |
| Frontend | React, HTML, CSS, JavaScript |
| Voice Input | SpeechRecognition (Python) |
| SMS Alerts | Twilio API |
| Location Detection | Geocoder (IP-based) |
| Data Storage | JSON |
| Deep Learning | PyTorch |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js (for React frontend)
- A Google Gemini API key
- A Twilio account (for panic button SMS feature)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/lekhalokare-28/Mind-Mate-Personalized-AI-Therapist.git
cd Mind-Mate-Personalized-AI-Therapist
```

2. **Install Python dependencies**
```bash
pip install google-generativeai nltk transformers torch speechrecognition geocoder fastapi uvicorn python-dotenv twilio pydantic requests keyboard
```

3. **Set up environment variables**

Create a `credentials.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

4. **Run the backend**
```bash
py therapist1.py
```

---

## 🎨 UI Screenshots

### 🏠 Landing Page
![Landing Page](Welcome%20or%20landing%20page)
*Welcome screen with Login and Sign Up options*

### 🔐 Login & Sign Up
![Login](Login)
*Returning user login screen*

![Sign Up](Sign%20up)
*New user registration with personal details*

### 📊 Dashboard
![Dashboard](Dashboard)
*Personalized dashboard with mood board, weekly mood graph, daily goals, and exercise suggestions*

### 💬 Chat Interface
![Chatbot Home](chatbot)
*Chat landing page with mood-based mindfulness suggestions*

![Chat](Chat%20interface%20with%20previous%20chats%20sidebar)
*Full chat interface with previous conversation history sidebar*

### 📓 Journal
![My Journal](My%20Journal)
*Journal entries grid — users can add unlimited journal pages*

![Journal Entry](Journal%20entry%20page)
*Individual journal entry with rich text editor and mood scale*

### 👤 User Profile
![User Profile](User%20profile)
*Profile page with personal info, helpline numbers, panic button toggle, and language settings*

---

## 📸 Backend Screenshots

### 👤 User Profile & First Session
![First Session](project%20pic%201(user%20record).PNG)
*New user session — username login and first-time greeting*

### 🧠 Conversation Memory
![Conversation Memory](project%20pic%207%20(user%20location%20service).PNG)
*MindMate remembers your previous emotional state and checks in on you*

### 🧘 Mindfulness Exercise (5-4-3-2-1 Grounding)
![Mindful Exercise](project%20pic%203(mindfull%20exercise%20recommendations).PNG)
*Suggests grounding techniques when anxiety or fear is detected*

### 🚨 Crisis Detection & Emergency Helplines
![Emergency Services](project%20pic%204(suggests%20emergency%20service%20numbers).PNG)
*Detects severe distress and immediately provides crisis helpline numbers*

### 📍 Location-Based Helplines (India)
![India Helplines](project%20pic%205(suggests%20emergency%20service%20numbers%20based%20on%20given%20location).PNG)
*Provides India-specific helplines including AASRA and Vandrevala Foundation*

### 🗺️ IP-Based Location Detection
![Location Detection](project%20pic%206%20(user%20location%20service).PNG)
*Automatically detects user location and tailors support resources accordingly*

### 😏 Sarcasm Detection
![Sarcasm Detection](project%20pic%208%20(Sarcasm%20emotion).PNG)
*Detects sarcasm in user responses and responds with empathy*

### 💬 Full Conversation Flow
![Full Conversation](project%20pic%202(user%20record).PNG)
*End-to-end conversation showing mood detection, sentiment analysis, and contextual responses*

---

## 👩‍💻 My Contribution

This is a collaborative project (2-member team). My contributions include:

- Designed and built the entire Python backend (`therapist1.py`)
- Integrated Google Gemini API with custom prompt engineering for therapeutic conversation
- Implemented dual sentiment analysis pipeline (VADER + DistilRoBERTa)
- Built user profile system with conversation memory and mood tracking
- Developed location-based emergency helpline suggestion using IP geolocation
- Integrated Twilio SMS panic button feature
- Implemented voice input using SpeechRecognition

My teammate handled the React frontend and backend-frontend integration.

---

## 🔮 Upcoming Features

- [ ] Full frontend-backend integration
- [ ] Doctor recommendation system for severe cases
- [ ] Improved mood analytics dashboard

---

## ⚠️ Disclaimer

MindMate is an AI-powered support tool and is **not a substitute for professional mental health care**. If you are experiencing a mental health crisis, please contact a licensed professional or call your local emergency services.

---

## 📬 Contact

**Lekha Ranjan Lokare**  
📧 lekhalokare.28@gmail.com  
🔗 [GitHub](https://github.com/lekhalokare-28)

---

> *"You don't have to face it alone."* 💙
