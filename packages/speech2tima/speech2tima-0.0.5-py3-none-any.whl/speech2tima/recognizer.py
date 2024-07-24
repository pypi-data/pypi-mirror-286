# speech2text/recognizer.py

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to listen to microphone and return recognized text
def gettext():
    with sr.Microphone() as source:
        print("Hi there!!\nI am Tima, your personal assistance waiting for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.05)  # Adjust microphone for ambient noise
        
        try:
            audio = recognizer.listen(source, timeout=2)  # Listen for audio input with timeout
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text.lower()  # Convert recognized text to lowercase
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None
