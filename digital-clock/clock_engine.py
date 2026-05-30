import pytz
from datetime import datetime
import time

class ClockEngine:
    """Engine for managing time and timezone conversions"""
    
    def __init__(self):
        self.timezones = []
        self.local_tz = pytz.timezone('UTC')
    
    def add_timezone(self, tz_name):
        """Add a timezone to the clock"""
        try:
            tz = pytz.timezone(tz_name)
            if tz_name not in self.timezones:
                self.timezones.append(tz_name)
            return True
        except Exception as e:
            print(f"Error adding timezone {tz_name}: {str(e)}")
            return False
    
    def remove_timezone(self, tz_name):
        """Remove a timezone from the clock"""
        if tz_name in self.timezones:
            self.timezones.remove(tz_name)
            return True
        return False
    
    def get_time_in_timezone(self, tz_name):
        """Get current time in a specific timezone"""
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            return now
        except Exception as e:
            print(f"Error getting time for {tz_name}: {str(e)}")
            return None
    
    def get_all_times(self):
        """Get current time in all configured timezones"""
        times = {}
        for tz_name in self.timezones:
            times[tz_name] = self.get_time_in_timezone(tz_name)
        return times
    
    def format_time(self, dt, time_format="%H:%M:%S", show_seconds=True):
        """Format datetime object to string"""
        if dt is None:
            return "--:--:--"
        
        if not show_seconds:
            return dt.strftime("%H:%M")
        return dt.strftime(time_format)
    
    def format_date(self, dt, date_format="%A, %B %d, %Y"):
        """Format date from datetime object"""
        if dt is None:
            return ""
        return dt.strftime(date_format)
    
    def get_utc_offset(self, tz_name):
        """Get UTC offset for a timezone"""
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            offset = now.strftime("%z")
            # Format as ±HH:MM
            return f"{offset[:-2]}:{offset[-2:]}"
        except Exception as e:
            print(f"Error getting offset for {tz_name}: {str(e)}")
            return "N/A"
    
    def get_timezone_abbreviation(self, tz_name):
        """Get timezone abbreviation (e.g., EST, PST)"""
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            return now.strftime("%Z")
        except Exception as e:
            print(f"Error getting abbreviation for {tz_name}: {str(e)}")
            return tz_name
    
    def get_all_available_timezones(self):
        """Get list of all available timezones"""
        return sorted(pytz.all_timezones)
    
    def get_time_difference(self, tz1_name, tz2_name):
        """Get time difference between two timezones in hours"""
        try:
            tz1 = pytz.timezone(tz1_name)
            tz2 = pytz.timezone(tz2_name)
            now_tz1 = datetime.now(tz1)
            now_tz2 = datetime.now(tz2)
            
            offset1 = now_tz1.utcoffset().total_seconds() / 3600
            offset2 = now_tz2.utcoffset().total_seconds() / 3600
            
            return offset2 - offset1
        except Exception as e:
            print(f"Error calculating difference: {str(e)}")
            return 0
    
    def is_dst(self, tz_name):
        """Check if timezone is in daylight saving time"""
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            return bool(now.dst())
        except Exception as e:
            print(f"Error checking DST for {tz_name}: {str(e)}")
            return False
