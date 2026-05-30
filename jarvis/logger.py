import logging
import os
from datetime import datetime
from config import Config

class JarvisLogger:
    def __init__(self, name="Jarvis"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(Config.LOG_LEVEL)
        
        # File handler
        log_file = os.path.join(Config.LOGS_PATH, f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(Config.LOG_LEVEL)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(Config.LOG_LEVEL)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger
