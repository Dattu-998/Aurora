from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from gtts import gTTS
import os
import time
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Google Gemini API
api_key = "AIzaSyA2fl6wsY-t88iTq8TpU2qfGhVRN2gzLeM"  # Replace with your actual API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"  # Use MongoDB Atlas URI if hosted online
client = MongoClient(MONGO_URI)
db = client["aurora_chat"]
chat_collection = db["chat_history"]

# Ensure 'static' folder exists
os.makedirs("static", exist_ok=True)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Generate AI response
        response = model.generate_content(user_message)
        bot_reply = response.text if response and hasattr(response, "text") else "I'm not sure how to respond."

        # Generate unique audio filename
        timestamp = int(time.time())
        audio_filename = f"response_{timestamp}.mp3"
        audio_path = os.path.join("static", audio_filename)

        # Convert text to speech and save
        try:
            tts = gTTS(bot_reply, lang="en")
            tts.save(audio_path)
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return jsonify({"error": "Failed to generate audio"}), 500

        # Store chat in MongoDB
        chat_entry = {
            "user": user_message,
            "bot": bot_reply,
            "audio": f"/static/{audio_filename}",
            "timestamp": timestamp
        }
        chat_collection.insert_one(chat_entry)

        return jsonify({"response": bot_reply, "audio": f"/static/{audio_filename}"})

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history():
    """Fetch chat history from MongoDB."""
    history = list(chat_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify({"history": history})

@app.route("/static/<filename>")
def send_audio(filename):
    return send_from_directory("static", filename, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
