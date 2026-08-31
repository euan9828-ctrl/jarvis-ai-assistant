# JARVIS AI Assistant

A sophisticated voice-enabled AI assistant inspired by JARVIS from Iron Man. This assistant can handle your daily tasks, respond to voice commands, manage reminders, and provide information queries.

## Features

✨ **Voice Recognition & Text-to-Speech**
- Listens to your voice commands
- Responds with natural speech synthesis
- Wake word activation ("Jarvis")

📋 **Task Management**
- Create and manage daily tasks
- Set priorities and due dates
- Mark tasks as complete
- Persistent task storage

⏰ **Reminders & Calendar**
- Set time-based reminders
- Recurring reminders
- Calendar integration (optional)
- Automatic notifications

🌐 **Information Queries**
- Weather information
- Current time and date
- News headlines
- General knowledge questions

🤖 **AI-Powered Conversations**
- Natural language processing
- Context-aware responses
- Powered by GPT-3.5-Turbo

🏠 **Smart Home Integration** (Optional)
- Control smart devices
- Home automation routines
- Voice-controlled lights, temperature, etc.

## Installation

### Prerequisites
- Python 3.8+
- Microphone and speakers
- OpenAI API key

### Setup Steps

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

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - OpenAI API key
   - Weather API key (optional)
   - Calendar API key (optional)

5. **Run JARVIS**
   ```bash
   python jarvis.py
   ```

## Usage

### Basic Voice Commands

**Wake up JARVIS:**
```
"Jarvis" → "Yes, sir? How may I assist you?"
```

**Task Management:**
```
"Jarvis, create a task to buy groceries"
"Jarvis, list my tasks"
"Jarvis, mark task 1 as complete"
"Jarvis, delete task 2"
```

**Reminders:**
```
"Jarvis, remind me to call mom in 1 hour"
"Jarvis, set a reminder for tomorrow at 9 AM"
"Jarvis, show my reminders"
```

**Information Queries:**
```
"Jarvis, what's the weather?"
"Jarvis, what time is it?"
"Jarvis, what's today's date?"
"Jarvis, get the latest news"
```

**Control:**
```
"Jarvis, stop" → Shut down
"Jarvis, help" → Show available commands
```

## Architecture

```
jarvis-ai-assistant/
├── jarvis.py              # Main application
├── voice_engine.py        # Speech recognition & TTS
├── ai_brain.py            # AI response generation
├── task_manager.py        # Task/reminder management
├── command_parser.py      # Natural language parsing
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── data/                 # Task/calendar storage
├── logs/                 # Application logs
└── utils/
    └── logger.py         # Logging setup
```

## Configuration

Edit `config.py` to customize:

- **Voice settings**: Rate, volume, language
- **Speech recognition**: Timeout, language
- **Task checking**: Interval for task checks
- **Wake word**: Change from "jarvis" to something else
- **Features**: Enable/disable weather, calendar, news, etc.

## API Integrations

### OpenAI (Required)
- Used for natural language processing and conversation
- Get API key from [platform.openai.com](https://platform.openai.com)

### Weather API (Optional)
- OpenWeatherMap or similar service
- Get API key from [openweathermap.org](https://openweathermap.org)

### News API (Optional)
- NewsAPI or similar service
- Get API key from [newsapi.org](https://newsapi.org)

### Google Calendar (Optional)
- For calendar integration and event management
- Setup OAuth2 credentials

## Troubleshooting

### Microphone Issues
- Check that microphone is properly connected
- Run with `--debug` flag for verbose output
- Test microphone: `python -c "import speech_recognition; print(speech_recognition.Microphone.list_microphone_indexes())"`

### API Key Errors
- Verify all API keys are correctly set in `.env`
- Check API key permissions and quotas
- Ensure keys are not expired

### Audio Output Issues
- Verify speakers are working
- Check volume settings in `config.py`
- Test with system audio settings

## Advanced Features (Coming Soon)

- 🏠 Smart home device control
- 📧 Email integration
- 📱 Mobile app companion
- 🧠 Machine learning for personalization
- 🔐 Enhanced security features
- 🌍 Multi-language support
- 🎵 Music playback integration

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Disclaimer

This project is inspired by JARVIS from Marvel's Iron Man universe. It is an educational and personal use project.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by Euan**

*"Good day, sir. I am at your service."*
