import sqlite3
import json
from datetime import datetime
from config import Config
from logger import JarvisLogger
import hashlib

logger = JarvisLogger().get_logger()

class LearningEngine:
    def __init__(self):
        self.db_path = Config.LEARNING_DB_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create learning table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_hash TEXT UNIQUE,
                    user_input TEXT,
                    response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 1,
                    feedback_score REAL DEFAULT 0.5,
                    category TEXT
                )
            ''')
            
            # Create patterns table for pattern matching
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT UNIQUE,
                    response_template TEXT,
                    confidence REAL DEFAULT 0.5,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 1
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Learning database initialized")
        except Exception as e:
            logger.error(f"Error initializing learning database: {str(e)}")
    
    def learn(self, user_input, response):
        """Store interaction for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            input_hash = hashlib.md5(user_input.lower().encode()).hexdigest()
            category = self._categorize_input(user_input)
            
            try:
                cursor.execute('''
                    INSERT INTO learned_interactions 
                    (input_hash, user_input, response, category)
                    VALUES (?, ?, ?, ?)
                ''', (input_hash, user_input, response, category))
            except sqlite3.IntegrityError:
                # Update if exists
                cursor.execute('''
                    UPDATE learned_interactions 
                    SET usage_count = usage_count + 1,
                        timestamp = CURRENT_TIMESTAMP
                    WHERE input_hash = ?
                ''', (input_hash,))
            
            # Enforce max learning entries
            cursor.execute('SELECT COUNT(*) FROM learned_interactions')
            count = cursor.fetchone()[0]
            if count > Config.MAX_LEARNING_ENTRIES:
                cursor.execute('''
                    DELETE FROM learned_interactions 
                    WHERE id IN (
                        SELECT id FROM learned_interactions 
                        ORDER BY feedback_score ASC, usage_count ASC 
                        LIMIT ?
                    )
                ''', (count - Config.MAX_LEARNING_ENTRIES,))
            
            conn.commit()
            conn.close()
            logger.info(f"Learned interaction: {user_input[:50]}")
        except Exception as e:
            logger.error(f"Error storing learning: {str(e)}")
    
    def get_context(self, user_input):
        """Retrieve learned context for user input"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            input_hash = hashlib.md5(user_input.lower().encode()).hexdigest()
            
            cursor.execute('''
                SELECT response, usage_count FROM learned_interactions 
                WHERE input_hash = ?
            ''', (input_hash,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return f"This query has been asked {result[1]} times before. Previous response was relevant."
            return None
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return None
    
    def _categorize_input(self, user_input):
        """Categorize user input"""
        keywords = {
            'system': ['cpu', 'memory', 'disk', 'process', 'system'],
            'file': ['file', 'folder', 'directory', 'open', 'create', 'delete'],
            'web': ['search', 'google', 'website', 'browser', 'internet'],
            'task': ['remind', 'schedule', 'alarm', 'timer', 'task'],
            'app': ['open', 'launch', 'run', 'application', 'program'],
            'general': ['hello', 'help', 'what', 'how', 'tell']
        }
        
        user_input_lower = user_input.lower()
        for category, words in keywords.items():
            if any(word in user_input_lower for word in words):
                return category
        return 'general'
    
    def get_stats(self):
        """Get learning statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM learned_interactions')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT category) FROM learned_interactions')
            categories = cursor.fetchone()[0]
            
            conn.close()
            return {"total_learned": total, "categories": categories}
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {}
