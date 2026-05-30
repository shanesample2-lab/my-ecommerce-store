# Jarvis - AI Assistant for Windows

A fully functional AI assistant with voice control, natural language processing, task automation, system monitoring, and self-learning capabilities.

## Features

### 🎤 Voice Control
- Wake word detection ("Jarvis" by default)
- Voice input recognition
- Text-to-speech responses
- Configurable voice properties

### 🧠 AI Brain
- OpenAI GPT-4 integration
- Natural language understanding
- Conversational context awareness
- Self-learning capabilities

### 📊 System Monitoring
- Real-time CPU usage monitoring
- Memory usage tracking
- Disk space analysis
- Process monitoring
- System health reports

### ⚙️ Task Automation
- Application launching
- File management
- Website opening
- Screenshots
- System control (shutdown, restart, lock)

### 📅 Task Scheduling
- Schedule tasks at specific times
- Create reminders
- Recurring tasks
- Task management

### 🧠 Self-Learning Engine
- Stores interaction history
- Learns from patterns
- Context-aware responses
- User preference adaptation

## Installation

### Prerequisites
- Python 3.8+
- Windows OS
- Microphone (for voice input)
- OpenAI API key
- ffmpeg (for audio processing)

### Quick Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
copy .env.example .env
# Edit .env and add your OpenAI API key

# 4. Test
python jarvis_main.py --interactive

# 5. Run
python jarvis_main.py
```

## Usage

### Voice Mode (Primary)
```bash
python jarvis_main.py
```

Listen for "Jarvis" wake word, then give your command.

### Interactive Text Mode (Testing)
```bash
python jarvis_main.py --interactive
```

Type commands directly without voice input.

## Example Commands

### System Information
- "What's my CPU usage?"
- "Show memory usage"
- "How much disk space do I have?"
- "System health"
- "Show running processes"

### Application Control
- "Open Chrome"
- "Open Notepad"
- "Open File Explorer"
- "Search for something on Google"

### File Management
- "Take a screenshot"
- "List files in downloads"
- "Create a file"

### System Control
- "Shutdown the computer in 60 seconds"
- "Restart"
- "Lock the computer"

### Reminders & Tasks
- "Remind me to take a break in 10 minutes"
- "Set a reminder for 3 PM"
- "Schedule a task"

## Configuration

Edit `.env` to customize:
- `OPENAI_API_KEY` - Your API key
- `JARVIS_NAME` - Assistant name
- `WAKE_WORD` - Wake word for activation
- `VOICE_GENDER` - male or female
- `VOICE_SPEED` - Speech speed (50-300)
- `DEBUG_MODE` - Enable debug logging

## How Self-Learning Works

1. **Recording**: Every interaction stored in SQLite
2. **Categorization**: Inputs categorized automatically
3. **Pattern Recognition**: Similar queries trigger learned context
4. **Optimization**: Frequent queries get refined responses
5. **Feedback**: System improves with usage

## Architecture

```
jarvis/
├── jarvis_main.py      # Entry point
├── voice_engine.py     # Voice I/O
├── brain.py            # AI processing
├── learning_engine.py  # Self-learning
├── command_handler.py  # Command routing
├── system_monitor.py   # System metrics
├── task_automation.py  # Task execution
├── task_scheduler.py   # Scheduling
├── config.py           # Configuration
├── logger.py           # Logging
├── requirements.txt    # Dependencies
├── .env.example       # Config template
└── README.md          # Documentation
```

## Troubleshooting

### Microphone Issues
- Ensure microphone is connected
- Check Windows audio settings
- Try interactive mode

### API Issues
- Verify API key in .env
- Check API key permissions
- Ensure account has credits

### Audio Issues
```bash
pip uninstall pyaudio
pip install pyaudio
```

## Performance Tips

- Use interactive mode for testing first
- Monitor API usage for costs
- Adjust VOICE_SPEED if too fast
- Regular database cleanup recommended

## Future Features

- [ ] Multi-language support
- [ ] Custom command creation
- [ ] Smart home integration
- [ ] Advanced scheduling
- [ ] Web dashboard
- [ ] Mobile control

## License

Open source - modify and use freely
