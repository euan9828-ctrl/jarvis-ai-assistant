# JARVIS AI Assistant 🤖

A voice-controlled AI assistant inspired by Tony Stark's JARVIS. Manage your daily tasks and respond to voice commands with natural language processing.

## Features ✨

- 🎤 **Voice Recognition** - Understand and respond to voice commands
- 🗣️ **Text-to-Speech** - Natural spoken responses
- ✅ **Task Management** - Add, list, complete, and delete tasks
- ⏰ **Reminders & Scheduling** - Set reminders and schedule events
- 🧠 **AI Brain** - Powered by Google Generative AI for intelligent responses
- 📋 **Data Persistence** - Tasks and reminders saved automatically
- 🌐 **Wikipedia Integration** - Quick facts and information

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- Microphone and speakers
- Internet connection (for AI features)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/euan9828-ctrl/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

5. **Run JARVIS**
   ```bash
   python main.py
   ```

## Getting Your API Key 🔑

### Google Generative AI API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file as `GOOGLE_API_KEY`

## Usage Examples 📝

### Task Management
```
"Add task buy groceries"
"List tasks"
"Complete task buy groceries"
"Delete task buy groceries"
```

### Time & Date
```
"What time is it?"
"What's today's date?"
```

### Reminders
```
"Set a reminder for 3 PM to call mom"
"Remind me to take out trash at 6 PM"
```

### General Questions
```
"What is machine learning?"
"Who is Elon Musk?"
"Tell me about Python"
```

### System
```
"Help"
"Status"
```

## Project Structure 📁

```
jarvis-ai-assistant/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore
├── README.md
├── modules/
│   ├── __init__.py
│   ├── voice_handler.py   # Speech recognition & TTS
│   ├── task_manager.py    # Task management
│   ├── ai_brain.py        # AI responses
│   └── scheduler.py       # Reminders & scheduling
└── data/
    ├── tasks.json         # Stored tasks
    └── reminders.json     # Stored reminders
```

## Architecture 🏗️

### Components

**VoiceHandler**
- Handles speech recognition using Google Speech Recognition
- Converts text to speech using pyttsx3
- Manages microphone input and speaker output

**TaskManager**
- CRUD operations for tasks
- Persistent JSON storage
- Task filtering and searching

**AIBrain**
- Natural language understanding
- Wikipedia integration for facts
- Google Generative AI for conversational responses

**TaskScheduler**
- Reminder scheduling
- Daily task checks
- Scheduled event management

## Configuration ⚙️

Edit `.env` file to customize:

```
GOOGLE_API_KEY=your_api_key
DEBUG=True/False
VOICE_RATE=150
VOICE_VOLUME=0.9
```

## Troubleshooting 🔧

### Microphone not detected
- Ensure microphone is connected and working
- Check system audio settings
- Try: `python -c "import pyaudio; pyaudio.PyAudio()"`

### Speech recognition not working
- Check internet connection (Google Speech Recognition requires it)
- Speak clearly and wait for the beep
- Check microphone is not muted

### API key errors
- Verify `GOOGLE_API_KEY` is set in `.env`
- Ensure the API key is valid
- Check API quotas and usage limits

### Audio playback issues
- Check speaker volume
- Verify speakers are connected
- Try: `python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"`

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Inspiration 💡

Inspired by JARVIS from the Iron Man films - A sophisticated AI assistant that's always there to help.

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by JARVIS**
