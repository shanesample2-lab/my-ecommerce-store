import openai
from config import Config
from logger import JarvisLogger
from learning_engine import LearningEngine

logger = JarvisLogger().get_logger()

class JarvisBrain:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.learning_engine = LearningEngine()
        self.conversation_history = []
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build the system prompt for Jarvis"""
        return f"""You are {Config.JARVIS_NAME}, an intelligent AI assistant for Windows. 
You are helpful, friendly, and knowledgeable about computer tasks, system management, and general information.
You can help with:
- File management and organization
- System monitoring and maintenance
- Task scheduling and reminders
- Web searches and information retrieval
- Application control and automation
- General conversation and assistance

Be concise, clear, and professional in your responses. Always be respectful and helpful."""
    
    def process_command(self, user_input):
        """Process user input and generate response"""
        try:
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get learned context
            learned_context = self.learning_engine.get_context(user_input)
            
            # Build messages with context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if learned_context:
                messages.append({
                    "role": "system",
                    "content": f"Previous learning: {learned_context}"
                })
            
            messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=Config.MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Learn from this interaction
            self.learning_engine.learn(user_input, assistant_message)
            
            logger.info(f"Response generated: {assistant_message[:100]}")
            return assistant_message
        
        except openai.error.AuthenticationError:
            logger.error("Invalid OpenAI API key")
            return "I'm sorry, I couldn't authenticate with the AI service. Please check your API key."
        except openai.error.RateLimitError:
            logger.error("Rate limit exceeded")
            return "I'm currently handling too many requests. Please try again in a moment."
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return f"I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
