import psutil
import os
from datetime import datetime
from logger import JarvisLogger

logger = JarvisLogger().get_logger()

class SystemMonitor:
    """Monitor system resources and performance"""
    
    @staticmethod
    def get_cpu_usage():
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage():
        """Get memory usage statistics"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024**3),
            'used': memory.used / (1024**3),
            'available': memory.available / (1024**3),
            'percent': memory.percent
        }
    
    @staticmethod
    def get_disk_usage(path='C:\\'):
        """Get disk usage statistics"""
        try:
            disk = psutil.disk_usage(path)
            return {
                'total': disk.total / (1024**3),
                'used': disk.used / (1024**3),
                'free': disk.free / (1024**3),
                'percent': disk.percent
            }
        except Exception as e:
            logger.error(f"Error getting disk usage: {str(e)}")
            return None
    
    @staticmethod
    def get_processes(limit=10):
        """Get top processes by CPU usage"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append({
                        'name': proc.info['name'],
                        'pid': proc.info['pid'],
                        'cpu_percent': proc.info['cpu_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
        except Exception as e:
            logger.error(f"Error getting processes: {str(e)}")
            return []
    
    @staticmethod
    def get_system_info():
        """Get general system information"""
        return {
            'platform': os.name,
            'cpu_count': psutil.cpu_count(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'uptime_seconds': int(datetime.now().timestamp() - psutil.boot_time())
        }
    
    @staticmethod
    def system_health_report():
        """Generate a system health report"""
        try:
            cpu = SystemMonitor.get_cpu_usage()
            memory = SystemMonitor.get_memory_usage()
            disk = SystemMonitor.get_disk_usage()
            
            report = f"""
System Health Report:
- CPU Usage: {cpu}%
- Memory Usage: {memory['percent']}% ({memory['used']:.2f}GB / {memory['total']:.2f}GB)
- Disk Usage: {disk['percent']}% ({disk['used']:.2f}GB / {disk['total']:.2f}GB free)
- Status: {'Healthy' if cpu < 80 and memory['percent'] < 80 and disk['percent'] < 90 else 'Warning'}
            """
            return report
        except Exception as e:
            logger.error(f"Error generating health report: {str(e)}")
            return "Unable to generate system health report"
