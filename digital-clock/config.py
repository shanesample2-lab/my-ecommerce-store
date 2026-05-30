# Digital Clock Configuration

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Multi-Timezone Digital Clock"
BG_COLOR = "#1a1a2e"
FG_COLOR = "#ffffff"

# Clock display settings
CLOCK_FONT_SIZE = 80
CLOCK_FONT = "Arial"
TIMEZONE_FONT_SIZE = 14
LABEL_FONT_SIZE = 16

# Timezone settings
DEFAULT_TIMEZONES = [
    "UTC",
    "US/Eastern",
    "US/Central",
    "US/Mountain",
    "US/Pacific",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Asia/Dubai",
    "Australia/Sydney",
    "Pacific/Auckland"
]

# Format settings
TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%A, %B %d, %Y"
HOUR_12 = False  # Set to True for 12-hour format

# Colors for different zones
TIMEZONE_COLORS = {
    "UTC": "#00ffff",
    "US/Eastern": "#ff6b6b",
    "US/Central": "#ffa94d",
    "US/Mountain": "#74b9ff",
    "US/Pacific": "#81ecec",
    "Europe/London": "#00b894",
    "Europe/Paris": "#fdcb6e",
    "Asia/Tokyo": "#ff7675",
    "Asia/Shanghai": "#fab1a0",
    "Asia/Dubai": "#a29bfe",
    "Australia/Sydney": "#55efc4",
    "Pacific/Auckland": "#ff6348"
}

# Update interval (milliseconds)
UPDATE_INTERVAL = 100

# Settings
SHOW_DATE = True
SHOW_SECONDS = True
SHOW_AM_PM = False  # Show AM/PM indicator
