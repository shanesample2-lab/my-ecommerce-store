import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MODEL = 'gpt-4'
    
    # Jarvis Configuration
    JARVIS_NAME = os.getenv('JARVIS_NAME', 'Jarvis')
    WAKE_WORD = os.getenv('WAKE_WORD', 'jarvis')
    
    # Voice Configuration
    VOICE_SPEED = int(os.getenv('VOICE_SPEED', 150))
    VOICE_GENDER = os.getenv('VOICE_GENDER', 'male')
    VOICE_VOLUME = 1.0
    
    # Speech Recognition
    RECOGNITION_TIMEOUT = 10
    RECOGNITION_PHRASE_TIME_LIMIT = 30
    
    # System Configuration
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Learning Configuration
    MAX_LEARNING_ENTRIES = int(os.getenv('MAX_LEARNING_ENTRIES', 10000))
    LEARNING_DB_PATH = 'jarvis/data/jarvis_learning.db'
    
    # Paths
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_PATH, 'data')
    LOGS_PATH = os.path.join(BASE_PATH, 'logs')
    
    # Create directories if they don't exist
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)
