from system_monitor import SystemMonitor
from task_automation import TaskAutomation
from task_scheduler import TaskScheduler
from logger import JarvisLogger
import re

logger = JarvisLogger().get_logger()

class CommandHandler:
    """Handle specific commands and route them appropriately"""
    
    def __init__(self):
        self.task_scheduler = TaskScheduler()
        self.task_scheduler.start_scheduler()
    
    def handle_command(self, user_input):
        """Handle direct commands"""
        user_input = user_input.lower().strip()
        
        # System monitoring commands
        if 'cpu' in user_input or 'processor' in user_input:
            cpu_usage = SystemMonitor.get_cpu_usage()
            return f"Current CPU usage is {cpu_usage}%"
        
        elif 'memory' in user_input or 'ram' in user_input:
            memory = SystemMonitor.get_memory_usage()
            return f"Memory usage: {memory['percent']}% ({memory['used']:.2f}GB / {memory['total']:.2f}GB)"
        
        elif 'disk' in user_input or 'storage' in user_input:
            disk = SystemMonitor.get_disk_usage()
            return f"Disk usage: {disk['percent']}% ({disk['used']:.2f}GB used, {disk['free']:.2f}GB free)"
        
        elif 'system health' in user_input or 'system status' in user_input:
            return SystemMonitor.system_health_report()
        
        elif 'processes' in user_input or 'running apps' in user_input:
            processes = SystemMonitor.get_processes()
            return "Top processes: " + ", ".join([f"{p['name']} ({p['cpu_percent']}%)" for p in processes[:5]])
        
        # Application commands
        elif 'open' in user_input:
            app_name = self._extract_app_name(user_input)
            if app_name:
                return TaskAutomation.open_application(app_name)
        
        elif 'browser' in user_input or 'website' in user_input or 'search' in user_input:
            url = self._extract_url(user_input)
            if url:
                return TaskAutomation.open_website(url)
        
        # File commands
        elif 'screenshot' in user_input or 'take picture' in user_input:
            return TaskAutomation.take_screenshot()
        
        elif 'list files' in user_input or 'show folder' in user_input:
            path = self._extract_path(user_input)
            files = TaskAutomation.list_directory(path)
            return "Files: " + ", ".join(files[:10])
        
        # System commands
        elif 'shutdown' in user_input:
            delay = self._extract_number(user_input)
            return TaskAutomation.shutdown_computer(delay)
        
        elif 'restart' in user_input:
            delay = self._extract_number(user_input)
            return TaskAutomation.restart_computer(delay)
        
        elif 'lock' in user_input:
            return TaskAutomation.lock_computer()
        
        # Reminder/Task commands
        elif 'remind' in user_input or 'reminder' in user_input:
            reminder_text = self._extract_reminder_text(user_input)
            minutes = self._extract_number(user_input)
            return f"Reminder set: {reminder_text}"
        
        else:
            return None
    
    def _extract_app_name(self, text):
        """Extract application name from text"""
        apps = ['chrome', 'firefox', 'notepad', 'calculator', 'file explorer', 'outlook', 'word', 'excel']
        for app in apps:
            if app in text:
                return app
        return None
    
    def _extract_url(self, text):
        """Extract URL from text"""
        # Simple URL extraction
        patterns = [
            r'(https?://[^\s]+)',
            r'(www\.[^\s]+)',
            r'([a-zA-Z0-9-]+\.[a-z]{2,})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def _extract_path(self, text):
        """Extract file path from text"""
        paths = [
            r'([A-Z]:\\[^\s]+)',
            r'(/[^\s]+)'
        ]
        for path_pattern in paths:
            match = re.search(path_pattern, text)
            if match:
                return match.group(1)
        return '.'
    
    def _extract_number(self, text):
        """Extract number from text"""
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0
    
    def _extract_reminder_text(self, text):
        """Extract reminder text"""
        if 'remind' in text:
            parts = text.split('remind')[1].split('in')[0].strip()
            return parts if parts else "Reminder"
        return "Reminder"
