# Digital Clock - Quick Start

## 5-Minute Setup

### 1. Install Python (if needed)
- Download from https://www.python.org/downloads/
- Version 3.7 or higher required

### 2. Install Dependencies
```bash
cd digital-clock
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

### 4. Manage Timezones
- **Add**: Click "+ Add Timezone" and search
- **Remove**: Click "- Remove Timezone" and select
- **Scroll**: Use mouse wheel or scrollbar

## Default Timezones

The clock displays these timezones by default:
- UTC
- US/Eastern (New York)
- US/Central (Chicago)
- US/Mountain (Denver)
- US/Pacific (Los Angeles)
- Europe/London (London)
- Europe/Paris (Paris)
- Asia/Tokyo (Tokyo)
- Asia/Shanghai (Shanghai)
- Asia/Dubai (Dubai)
- Australia/Sydney (Sydney)
- Pacific/Auckland (Auckland)

## Quick Customization

Edit `config.py` to change:

**Window Size:**
```python
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
```

**Clock Size:**
```python
CLOCK_FONT_SIZE = 80  # Increase for larger display
```

**Time Format (12-hour):**
```python
HOUR_12 = True
TIME_FORMAT = "%I:%M:%S %p"
```

**Default Timezones:**
```python
DEFAULT_TIMEZONES = [
    "UTC",
    "US/Eastern",
    "US/Pacific",
    "Asia/Tokyo",
]
```

## Common Tasks

### Add a New Timezone
1. Click "+ Add Timezone"
2. Type timezone name (e.g., "Asia/Bangkok")
3. Double-click to select

### Change Display Colors
Edit in `config.py`:
```python
TIMEZONE_COLORS = {
    "UTC": "#00ffff",           # Cyan
    "US/Eastern": "#ff6b6b",    # Red
    "US/Pacific": "#81ecec",    # Light Blue
}
```

### Hide Date/Seconds
Edit in `config.py`:
```python
SHOW_DATE = False
SHOW_SECONDS = False
TIME_FORMAT = "%H:%M"  # Show only hours and minutes
```

## Popular Timezone Codes

```
US/Eastern      - Eastern Time (New York)
US/Central      - Central Time (Chicago)
US/Mountain     - Mountain Time (Denver)
US/Pacific      - Pacific Time (Los Angeles)
Europe/London   - Greenwich Mean Time (London)
Europe/Paris    - Central European Time (Paris)
Asia/Tokyo      - Japan Standard Time (Tokyo)
Asia/Shanghai   - China Standard Time (Shanghai)
Australia/Sydney - Australian Eastern Time (Sydney)
Pacific/Auckland - New Zealand Standard Time
```

## Keyboard Shortcuts

- **Mouse Wheel**: Scroll through timezones
- **Double-Click**: Select timezone in dialog
- **Escape**: Close timezone selector

## Tips

1. **For Many Timezones**: Reduce `CLOCK_FONT_SIZE` in config
2. **For Few Timezones**: Increase `CLOCK_FONT_SIZE`
3. **Mobile Usage**: Reduce window size in config
4. **Remote Display**: Keep default colors for visibility

## Troubleshooting

**Application won't start:**
```bash
pip install --upgrade pytz
python main.py
```

**Can't find timezone:**
- Use the search box in timezone selector
- Check spelling (case-sensitive)
- Visit pytz docs for complete list

**Display too small/large:**
- Adjust `CLOCK_FONT_SIZE` in config
- Resize window in `WINDOW_WIDTH` and `WINDOW_HEIGHT`

## Next Steps

1. Customize colors to match your style
2. Set default timezones for your use case
3. Adjust clock size for your display
4. Pin to taskbar for quick access

Enjoy your multi-timezone clock! ⏰
