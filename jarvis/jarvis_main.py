#!/usr/bin/env python3
"""
Jarvis - AI Assistant for Windows
A fully functional AI assistant with voice control, task automation, and self-learning capabilities
"""

import time
import sys
from voice_engine import VoiceEngine
from brain import JarvisBrain
from command_handler import CommandHandler
from system_monitor import SystemMonitor
from logger import JarvisLogger
from config import Config

logger = JarvisLogger().get_logger()

class Jarvis:
    def __init__(self):
        logger.info("Initializing Jarvis...")
        
        # Check API key
        if not Config.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not set in .env file")
            print("ERROR: Please set OPENAI_API_KEY in .env file")
            sys.exit(1)
        
        self.voice_engine = VoiceEngine()
        self.brain = JarvisBrain()
        self.command_handler = CommandHandler()
        self.running = False
        
        logger.info("Jarvis initialized successfully")
    
    def start(self):
        """Start Jarvis"""
        self.running = True
        self.voice_engine.speak(f"Hello, I'm {Config.JARVIS_NAME}. I'm ready to help. Say {Config.WAKE_WORD} to get my attention.")
        logger.info(f"{Config.JARVIS_NAME} started")
        
        while self.running:
            try:
                # Listen for wake word
                user_input = self.voice_engine.listen()
                
                if user_input is None:
                    continue
                
                # Check for wake word
                if not self.voice_engine.is_wake_word(user_input):
                    continue
                
                # Wake word detected
                self.voice_engine.speak("I'm listening")
                
                # Listen for command
                command = self.voice_engine.listen()
                
                if command is None:
                    self.voice_engine.speak("I didn't catch that. Please repeat.")
                    continue
                
                # Process command
                response = self._process_command(command)
                
                # Speak response
                self.voice_engine.speak(response)
                
                logger.info(f"Command processed: {command}")
                
            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                self.voice_engine.speak("An error occurred. Please try again.")
    
    def _process_command(self, command):
        """Process user command"""
        # Try specific command handler first
        specific_response = self.command_handler.handle_command(command)
        if specific_response:
            return specific_response
        
        # Fall back to AI brain
        return self.brain.process_command(command)
    
    def stop(self):
        """Stop Jarvis"""
        self.running = False
        self.voice_engine.speak(f"Goodbye! {Config.JARVIS_NAME} is shutting down.")
        self.command_handler.task_scheduler.stop_scheduler()
        logger.info(f"{Config.JARVIS_NAME} stopped")
        sys.exit(0)
    
    def interactive_mode(self):
        """Run in interactive text mode (for testing without microphone)"""
        self.running = True
        print(f"\n{Config.JARVIS_NAME} Interactive Mode")
        print("=" * 50)
        print(f"Commands: type 'help' for commands, 'exit' to quit\n")
        
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print(f"{Config.JARVIS_NAME}: Goodbye!")
                    self.stop()
                
                elif user_input.lower() == 'help':
                    self._print_help()
                
                elif user_input.lower() == 'status':
                    print(SystemMonitor.system_health_report())
                
                elif user_input.lower() == 'stats':
                    stats = self.brain.learning_engine.get_stats()
                    print(f"Learning Stats: {stats}")
                
                else:
                    response = self._process_command(user_input)
                    print(f"{Config.JARVIS_NAME}: {response}\n")
                
            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")
                print(f"Error: {str(e)}")
    
    def _print_help(self):
        """Print help information"""
        help_text = """
Commands:
  status           - Show system health
  stats            - Show learning statistics
  exit             - Exit Jarvis
  help             - Show this help message

Example commands:
  - "what's my CPU usage?"
  - "show memory usage"
  - "open chrome"
  - "take a screenshot"
  - "show system health"
  - "remind me to take a break in 10 minutes"
        """
        print(help_text)

def main():
    """Main entry point"""
    try:
        jarvis = Jarvis()
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            jarvis.interactive_mode()
        else:
            jarvis.start()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
