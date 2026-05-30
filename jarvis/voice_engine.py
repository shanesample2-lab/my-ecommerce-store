import pyttsx3
import speech_recognition as sr
from config import Config
from logger import JarvisLogger

logger = JarvisLogger().get_logger()

class VoiceEngine:
    def __init__(self):
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', Config.VOICE_SPEED)
        self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)
        
        # Set voice gender
        voices = self.tts_engine.getProperty('voices')
        if Config.VOICE_GENDER.lower() == 'female':
            self.tts_engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        else:
            self.tts_engine.setProperty('voice', voices[0].id if len(voices) > 0 else voices[0].id)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def speak(self, text):
        """Convert text to speech and play it"""
        try:
            logger.info(f"Jarvis: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Error speaking: {str(e)}")
    
    def listen(self, timeout=Config.RECOGNITION_TIMEOUT):
        """Listen to microphone and convert speech to text"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=Config.RECOGNITION_PHRASE_TIME_LIMIT)
            
            # Recognize speech using Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {str(e)}")
                return None
        except sr.RequestError as e:
            logger.error(f"Microphone error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error listening: {str(e)}")
            return None
    
    def is_wake_word(self, text):
        """Check if wake word is in the text"""
        return Config.WAKE_WORD.lower() in text if text else False
