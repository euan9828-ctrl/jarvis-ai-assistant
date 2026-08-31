import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CALENDAR_API_KEY = os.getenv('CALENDAR_API_KEY')

# Voice Settings
VOICE_RATE = 150  # Words per minute
VOICE_VOLUME = 0.9  # 0.0 to 1.0
VOICE_LANGUAGE = 'en-US'

# Speech Recognition Settings
SPEECH_RECOGNITION_TIMEOUT = 10  # seconds
SPEECH_RECOGNITION_LANGUAGE = 'en-US'

# Tasks Configuration
TASK_CHECK_INTERVAL = 60  # seconds
MAX_RETRY_ATTEMPTS = 3

# Wake Word
WAKE_WORD = 'jarvis'
WAKE_WORD_CONFIDENCE = 0.8

# Database
TASK_DB_PATH = 'data/tasks.json'
CALENDAR_DB_PATH = 'data/calendar.json'

# Features Enabled
ENABLE_WEATHER = True
ENABLE_CALENDAR = True
ENABLE_NEWS = True
ENABLE_REMINDERS = True
ENABLE_SMART_HOME = False
