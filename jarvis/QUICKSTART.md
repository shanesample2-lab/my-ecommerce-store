# Jarvis Quick Start Guide

## 5-Minute Setup

### 1. Get OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy it

### 2. Setup Jarvis
```bash
cd jarvis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure
```bash
copy .env.example .env
```

Edit `.env` and add your API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### 4. Test (Text Mode)
```bash
python jarvis_main.py --interactive
```

Type: `status` then press Enter

### 5. Run (Voice Mode)
```bash
python jarvis_main.py
```

Say "Jarvis" then your command

## Commands to Try

### System Info
```
status           - System health
cpu usage        - CPU percentage
memory           - RAM usage
disk             - Storage info
```

### Applications
```
open chrome      - Launch Chrome
open notepad     - Open Notepad
```

### Files
```
screenshot       - Capture screen
list files       - Show files
```

### Help
```
help             - Show commands
stats            - Learning stats
```

## Troubleshooting

**No sound?**
- Check Windows volume
- Test speakers work

**Can't hear Jarvis?**
- Edit `.env`: `VOICE_GENDER=female`
- Adjust `VOICE_SPEED`

**API error?**
- Check API key in `.env`
- Verify it's valid at openai.com

**Microphone not working?**
- Use interactive mode: `python jarvis_main.py --interactive`
- Check microphone in Windows settings
