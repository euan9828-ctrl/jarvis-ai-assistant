import speech_recognition as sr
import pyttsx3
import logging
from config import *

logger = logging.getLogger('jarvis')

class VoiceEngine:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)
        
        logger.info("Voice Engine initialized")
    
    def listen(self, timeout=SPEECH_RECOGNITION_TIMEOUT):
        """Listen for audio input"""
        try:
            with self.microphone as source:
                logger.info("Listening for audio...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                return audio
        except sr.RequestError as e:
            logger.error(f"Could not request results; {e}")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
    
    def recognize_speech(self, audio):
        """Convert speech to text"""
        try:
            text = self.recognizer.recognize_google(
                audio,
                language=SPEECH_RECOGNITION_LANGUAGE
            )
            logger.info(f"Recognized speech: {text}")
            return text
        except sr.RequestError as e:
            logger.error(f"Could not request results; {e}")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
    
    def cleanup(self):
        """Clean up voice engine resources"""
        try:
            self.engine.stop()
            logger.info("Voice Engine cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
