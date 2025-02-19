import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import datetime
import json
from typing import List, Optional
import sys
import asyncio
import websockets
import json
import os
import base64
from dotenv import load_dotenv
import pyaudio
import numpy as np

# Debug environment variables
print("Debug: .env file path:", os.path.join(os.getcwd(), '.env'))
load_dotenv(verbose=True)  # Add verbose=True to see loading details

# Load environment variables first
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
API_VERSION = "2024-10-01-preview"

# Then print the loaded values
print("Loaded environment variables:")
print(f"ENDPOINT: {ENDPOINT}")
print(f"DEPLOYMENT: {DEPLOYMENT}")
print(f"API_KEY: {'Set' if API_KEY else 'Not set'}")

# After load_dotenv()
if not all([API_KEY, ENDPOINT, DEPLOYMENT]):
    print(f"Environment variables status:")
    print(f"API_KEY: {'Set' if API_KEY else 'Not set'}")
    print(f"ENDPOINT: {ENDPOINT or 'Not set'}")
    print(f"DEPLOYMENT: {DEPLOYMENT or 'Not set'}")
    sys.exit("Missing required environment variables")

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize PyAudio
audio = pyaudio.PyAudio()

def stream_audio(ws):
    """Stream microphone audio to WebSocket."""
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    try:
        while True:
            data = stream.read(CHUNK)
            encoded_audio = base64.b64encode(data).decode("utf-8")
            asyncio.run(ws.send(json.dumps({"type": "audio", "data": encoded_audio})))
    except Exception as e:
        print(f"Error streaming audio: {e}")
    finally:
        stream.stop_stream()
        stream.close()

async def connect_to_realtime_api():
    if not ENDPOINT or not DEPLOYMENT:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT must be set")
    
    # Convert HTTPS endpoint to WSS
    ws_endpoint = ENDPOINT.replace('https://', 'wss://')
    url = f"{ws_endpoint}/openai/realtime?api-version={API_VERSION}&deployment={DEPLOYMENT}"
    
    headers = {
        "api-key": API_KEY
    }

    try:
        # Create connection with headers in the URL
        async with websockets.connect(
            url,
            extra_headers=headers,
            subprotocols=['wss']
        ) as websocket:
            # Your WebSocket logic here
            while True:
                # Handle your WebSocket communication
                pass
    except Exception as e:
        print(f"WebSocket connection error: {e}")

# Run the client
asyncio.run(connect_to_realtime_api())


# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class ConversationBot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.conversation = []
        self.user_info = {}
        self.questions = [
            "What's your name?",
            "When were you born?",
            "Where did you grow up?",
            "Which high school did you attend?",
            "What are your hobbies?",
            "What do you do for work?",
            "Do you have any siblings?",
            "What's your favorite food?",
        ]
        self.asked_questions = set()

    def speak(self, text):
        print("Bot:", text)
        self.engine.say(text)
        self.engine.runAndWait()
        self.conversation.append({"bot": text})

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print("You:", text)
                self.conversation.append({"user": text})
                return text.lower()
            except:
                self.speak("Sorry, I didn't catch that. Could you please repeat?")
                return self.listen()

    def is_end_conversation(self, text):
        end_phrases = ["i'm done", "that's all for now", "goodbye", "bye"]
        return any(phrase in text.lower() for phrase in end_phrases)

    def save_conversation(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.conversation, f, indent=2)
        print(f"Conversation saved to {filename}")

    def get_next_question(self):
        available_questions = [q for q in self.questions if q not in self.asked_questions]
        if available_questions:
            question = available_questions[0]
            self.asked_questions.add(question)
            return question
        return "Is there anything else you'd like to share?"

    def start_conversation(self):
        self.speak("Hello! I'd love to get to know you better.")
        
        while True:
            question = self.get_next_question()
            self.speak(question)
            
            response = self.listen()
            
            if self.is_end_conversation(response):
                self.speak("It was nice talking to you! Goodbye!")
                break
        
        self.save_conversation()

if __name__ == "__main__":
    bot = ConversationBot()
    bot.start_conversation()

# Example usage:
text = "Hello! How are you doing today? NLTK is great for text processing."
sentences = sent_tokenize(text)
words = word_tokenize(text)

import nltk
import speech_recognition as sr
from typing import List, Optional
import sys

def process_speech() -> Optional[List[str]]:
    """
    Captures speech from microphone, converts to text, and returns tokenized words.
    
    Returns:
        List[str]: Tokenized words from speech, or None if processing fails
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"Recognized text: {text}")
            tokens = nltk.word_tokenize(text)
            return tokens
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        
        import sys
print(f"Python path: {sys.executable}")
print(f"Python version: {sys.version}")