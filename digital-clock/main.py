#!/usr/bin/env python3
"""
Multi-Timezone Digital Clock
Displays current time across multiple timezones with a modern GUI
"""

import tkinter as tk
from tkinter import messagebox
from clock_engine import ClockEngine
from ui_components import ClockDisplay, ControlPanel, TimezoneSelector
from config import *
import pytz

class DigitalClockApp:
    """Main application for multi-timezone digital clock"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.config(bg=BG_COLOR)
        
        # Initialize clock engine
        self.clock_engine = ClockEngine()
        for tz in DEFAULT_TIMEZONES:
            self.clock_engine.add_timezone(tz)
        
        # Clock displays dictionary
        self.clock_displays = {}
        
        # Create UI
        self._create_ui()
        
        # Start update loop
        self._update_clocks()
    
    def _create_ui(self):
        """Create user interface"""
        # Top control panel
        self.control_panel = ControlPanel(
            self.root,
            self._on_add_timezone,
            self._on_remove_timezone
        )
        
        # Main clock container with scrollbar
        container_frame = tk.Frame(self.root, bg=BG_COLOR)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas with scrollbar for clocks
        canvas = tk.Canvas(
            container_frame,
            bg=BG_COLOR,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.scroll)
        self.scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Add initial clock displays
        self._refresh_clock_displays()
    
    def _refresh_clock_displays(self):
        """Refresh all clock displays"""
        # Clear existing displays
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.clock_displays.clear()
        
        # Create grid of clock displays
        cols = 3
        row = 0
        col = 0
        
        for tz_name in self.clock_engine.timezones:
            tz_color = TIMEZONE_COLORS.get(tz_name, "#ffffff")
            clock_display = ClockDisplay(self.scrollable_frame, tz_name, tz_color)
            
            clock_frame = clock_display.get_frame()
            clock_frame.grid(
                row=row,
                column=col,
                padx=20,
                pady=20,
                sticky="nsew"
            )
            
            self.clock_displays[tz_name] = clock_display
            
            col += 1
            if col >= cols:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(cols):
            self.scrollable_frame.columnconfigure(i, weight=1)
    
    def _update_clocks(self):
        """Update all clock displays"""
        times = self.clock_engine.get_all_times()
        
        for tz_name, dt in times.items():
            if tz_name in self.clock_displays:
                time_str = self.clock_engine.format_time(
                    dt,
                    TIME_FORMAT if SHOW_SECONDS else "%H:%M",
                    SHOW_SECONDS
                )
                
                date_str = ""
                if SHOW_DATE:
                    date_str = self.clock_engine.format_date(dt, DATE_FORMAT)
                
                offset_str = self.clock_engine.get_utc_offset(tz_name)
                abbr = self.clock_engine.get_timezone_abbreviation(tz_name)
                offset_str = f"{abbr} (UTC{offset_str})"
                
                self.clock_displays[tz_name].update(
                    time_str,
                    date_str,
                    offset_str
                )
        
        # Schedule next update
        self.root.after(UPDATE_INTERVAL, self._update_clocks)
    
    def _on_add_timezone(self):
        """Handle add timezone button"""
        available = self.clock_engine.get_all_available_timezones()
        # Filter out already added timezones
        available = [tz for tz in available if tz not in self.clock_engine.timezones]
        
        if not available:
            messagebox.showwarning("No Timezones", "All timezones are already added!")
            return
        
        def on_timezone_selected(tz_name):
            if self.clock_engine.add_timezone(tz_name):
                self._refresh_clock_displays()
                messagebox.showinfo("Success", f"Added timezone: {tz_name}")
            else:
                messagebox.showerror("Error", f"Failed to add timezone: {tz_name}")
        
        TimezoneSelector(self.root, available, on_timezone_selected)
    
    def _on_remove_timezone(self):
        """Handle remove timezone button"""
        if not self.clock_engine.timezones:
            messagebox.showwarning("No Timezones", "No timezones to remove!")
            return
        
        def on_timezone_selected(tz_name):
            if self.clock_engine.remove_timezone(tz_name):
                self._refresh_clock_displays()
                messagebox.showinfo("Success", f"Removed timezone: {tz_name}")
            else:
                messagebox.showerror("Error", f"Failed to remove timezone: {tz_name}")
        
        TimezoneSelector(self.root, self.clock_engine.timezones, on_timezone_selected)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DigitalClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
