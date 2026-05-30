import subprocess
import os
import webbrowser
from logger import JarvisLogger
import pyautogui
import time

logger = JarvisLogger().get_logger()

class TaskAutomation:
    """Automate common system tasks"""
    
    @staticmethod
    def open_application(app_name):
        """Open an application by name"""
        try:
            if app_name.lower() == 'chrome':
                subprocess.Popen('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
            elif app_name.lower() == 'firefox':
                subprocess.Popen('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
            elif app_name.lower() == 'notepad':
                subprocess.Popen('notepad.exe')
            elif app_name.lower() == 'calculator':
                subprocess.Popen('calc.exe')
            elif app_name.lower() == 'file explorer':
                subprocess.Popen('explorer.exe')
            else:
                subprocess.Popen(app_name)
            
            logger.info(f"Opened application: {app_name}")
            return f"Opening {app_name}"
        except Exception as e:
            logger.error(f"Error opening application: {str(e)}")
            return f"Unable to open {app_name}"
    
    @staticmethod
    def open_website(url):
        """Open a website in default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            logger.info(f"Opened website: {url}")
            return f"Opening {url}"
        except Exception as e:
            logger.error(f"Error opening website: {str(e)}")
            return "Unable to open website"
    
    @staticmethod
    def take_screenshot():
        """Take a screenshot of the desktop"""
        try:
            timestamp = int(time.time())
            screenshot_path = f"C:\\Users\\{os.getenv('USERNAME')}\\Pictures\\screenshot_{timestamp}.png"
            pyautogui.screenshot(screenshot_path)
            logger.info(f"Screenshot taken: {screenshot_path}")
            return f"Screenshot saved to {screenshot_path}"
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            return "Unable to take screenshot"
    
    @staticmethod
    def create_file(filename, content=''):
        """Create a file with content"""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            logger.info(f"File created: {filename}")
            return f"File created: {filename}"
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            return "Unable to create file"
    
    @staticmethod
    def delete_file(filepath):
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
                return f"File deleted: {filepath}"
            else:
                return "File not found"
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return "Unable to delete file"
    
    @staticmethod
    def list_directory(path='.'):
        """List contents of a directory"""
        try:
            contents = os.listdir(path)
            logger.info(f"Listed directory: {path}")
            return contents
        except Exception as e:
            logger.error(f"Error listing directory: {str(e)}")
            return []
    
    @staticmethod
    def shutdown_computer(delay=0):
        """Shutdown the computer"""
        try:
            subprocess.Popen(f'shutdown /s /t {delay}')
            logger.warning(f"Computer shutdown initiated with {delay} second delay")
            return f"Computer will shutdown in {delay} seconds"
        except Exception as e:
            logger.error(f"Error shutting down: {str(e)}")
            return "Unable to shutdown computer"
    
    @staticmethod
    def restart_computer(delay=0):
        """Restart the computer"""
        try:
            subprocess.Popen(f'shutdown /r /t {delay}')
            logger.warning(f"Computer restart initiated with {delay} second delay")
            return f"Computer will restart in {delay} seconds"
        except Exception as e:
            logger.error(f"Error restarting: {str(e)}")
            return "Unable to restart computer"
    
    @staticmethod
    def lock_computer():
        """Lock the computer"""
        try:
            subprocess.Popen('rundll32.exe user32.dll,LockWorkStation')
            logger.info("Computer locked")
            return "Computer locked"
        except Exception as e:
            logger.error(f"Error locking computer: {str(e)}")
            return "Unable to lock computer"
