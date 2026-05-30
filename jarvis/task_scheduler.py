import schedule
import time
from datetime import datetime, timedelta
from logger import JarvisLogger
import threading

logger = JarvisLogger().get_logger()

class TaskScheduler:
    """Schedule and manage tasks"""
    
    def __init__(self):
        self.tasks = {}
        self.scheduler_thread = None
        self.running = False
    
    def schedule_task(self, task_name, task_func, schedule_time=None, interval=None):
        """
        Schedule a task
        schedule_time: "HH:MM" format for daily tasks
        interval: seconds for recurring tasks
        """
        try:
            self.tasks[task_name] = {
                'function': task_func,
                'schedule_time': schedule_time,
                'interval': interval,
                'created_at': datetime.now(),
                'last_run': None,
                'next_run': None
            }
            
            if schedule_time:
                schedule.every().day.at(schedule_time).do(task_func)
                self.tasks[task_name]['next_run'] = self._calculate_next_run(schedule_time)
            elif interval:
                schedule.every(interval).seconds.do(task_func)
                self.tasks[task_name]['next_run'] = datetime.now() + timedelta(seconds=interval)
            
            logger.info(f"Task scheduled: {task_name}")
        except Exception as e:
            logger.error(f"Error scheduling task: {str(e)}")
    
    def create_reminder(self, reminder_text, minutes=None, hours=None, days=None):
        """Create a reminder"""
        try:
            if minutes:
                delay = timedelta(minutes=minutes)
            elif hours:
                delay = timedelta(hours=hours)
            elif days:
                delay = timedelta(days=days)
            else:
                delay = timedelta(minutes=1)
            
            run_time = datetime.now() + delay
            reminder_id = f"reminder_{datetime.now().timestamp()}"
            
            def reminder_task():
                logger.info(f"Reminder: {reminder_text}")
                return reminder_text
            
            self.schedule_task(reminder_id, reminder_task, interval=int(delay.total_seconds()))
            logger.info(f"Reminder created: {reminder_text}")
            return reminder_id
        except Exception as e:
            logger.error(f"Error creating reminder: {str(e)}")
    
    def start_scheduler(self):
        """Start the task scheduler in a background thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            logger.info("Task scheduler started")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self.running = False
        logger.info("Task scheduler stopped")
    
    def list_tasks(self):
        """List all scheduled tasks"""
        return self.tasks
    
    def cancel_task(self, task_name):
        """Cancel a scheduled task"""
        if task_name in self.tasks:
            del self.tasks[task_name]
            logger.info(f"Task cancelled: {task_name}")
    
    def _calculate_next_run(self, schedule_time):
        """Calculate next run time for a scheduled task"""
        try:
            hour, minute = map(int, schedule_time.split(':'))
            now = datetime.now()
            next_run = now.replace(hour=hour, minute=minute, second=0)
            
            if next_run <= now:
                next_run += timedelta(days=1)
            
            return next_run
        except Exception as e:
            logger.error(f"Error calculating next run: {str(e)}")
            return None
