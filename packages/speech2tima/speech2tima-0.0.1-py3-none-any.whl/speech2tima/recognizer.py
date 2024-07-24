# speech2text/recognizer.py

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to listen to microphone and return recognized text
def listen_microphone():
    with sr.Microphone() as source:
        print("Tima is Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust microphone for ambient noise
        
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for audio input with timeout
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text.lower()  # Convert recognized text to lowercase
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

# Main function to continuously listen for voice input
def main():
    while True:
        print("\nSay something or say 'close' to quit:")
        input_text = listen_microphone()
        
        if input_text:
            print(f"You said: {input_text}")
            if 'close' in input_text:
                print("Closing...")
                break
