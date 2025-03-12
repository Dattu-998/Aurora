import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# 🔹 Step 1: Set up the Gemini API
genai.configure(api_key="AIzaSyANKkeejIAj6tr-ekfXw6uPUIr1mVGW2QE")  # Replace with your API key

# 🔹 Step 2: Initialize the AI model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 🔹 Step 3: Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust voice speed

# 🔹 Step 4: Speech Recognition
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    """Capture user voice input and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            print("You:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            print("Speech Recognition service error.")
            return None

def chat_with_aurora(user_input):
    """Send user input to Gemini AI and get response."""
    try:
        response = model.generate_content(user_input)
        reply = response.text.strip()
        print("Aurora:", reply)
        speak(reply)
    except Exception as e:
        print("Error:", e)

# 🔹 Main Loop
while True:
    print("\nType your message or say 'voice' to speak (type 'exit' to quit).")
    choice = input(">> ").strip().lower()

    if choice == "exit":
        print("Goodbye!")
        break
    elif choice == "voice":
        user_input = get_voice_input()
    else:
        user_input = choice

    if user_input:
        chat_with_aurora(user_input)
