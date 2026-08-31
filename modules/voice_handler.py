"""
Voice Handler Module - Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import os


class VoiceHandler:
    """Handles voice input and output"""
    
    def __init__(self):
        """Initialize voice handler with recognizer and engine"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure text-to-speech engine
        self.engine.setProperty('rate', 150)  # Speech rate
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Set voice (can be male or female)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # 1 for female, 0 for male
        
        print("✓ Voice handler initialized")
    
    def listen(self, timeout=5):
        """
        Listen for voice input from microphone
        
        Args:
            timeout (int): Timeout in seconds
            
        Returns:
            str: Recognized text or empty string if recognition failed
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio
                print("🎙️ Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Recognize speech using Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"✓ Recognized: {text}")
                return text
            
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return ""
            
            except sr.RequestError as e:
                print(f"❌ API error: {str(e)}")
                return ""
        
        except sr.RequestError as e:
            print(f"❌ Microphone error: {str(e)}")
            return ""
        except Exception as e:
            print(f"❌ Voice input error: {str(e)}")
            return ""
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to speak
        """
        try:
            print(f"🗣️ Speaking: {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Text-to-speech error: {str(e)}")
    
    def listen_continuous(self, callback, stop_event):
        """
        Listen continuously in background
        
        Args:
            callback (function): Function to call with recognized text
            stop_event (threading.Event): Event to stop listening
        """
        while not stop_event.is_set():
            text = self.listen(timeout=2)
            if text:
                callback(text)
