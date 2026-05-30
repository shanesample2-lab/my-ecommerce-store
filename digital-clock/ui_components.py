import tkinter as tk
from tkinter import font
from config import *

class ClockDisplay:
    """Display component for a single timezone clock"""
    
    def __init__(self, parent, tz_name, tz_color="#ffffff"):
        self.parent = parent
        self.tz_name = tz_name
        self.tz_color = tz_color
        self.frame = tk.Frame(parent, bg=BG_COLOR)
        
        # Create widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create clock display widgets"""
        # Timezone label
        self.tz_label = tk.Label(
            self.frame,
            text=self.tz_name,
            font=(CLOCK_FONT, TIMEZONE_FONT_SIZE, "bold"),
            fg=self.tz_color,
            bg=BG_COLOR
        )
        self.tz_label.pack(pady=5)
        
        # Time display
        self.time_label = tk.Label(
            self.frame,
            text="00:00:00",
            font=(CLOCK_FONT, CLOCK_FONT_SIZE, "bold"),
            fg=self.tz_color,
            bg=BG_COLOR
        )
        self.time_label.pack()
        
        # Date display
        self.date_label = tk.Label(
            self.frame,
            text="",
            font=(CLOCK_FONT, LABEL_FONT_SIZE),
            fg=self.tz_color,
            bg=BG_COLOR
        )
        self.date_label.pack(pady=5)
        
        # UTC offset display
        self.offset_label = tk.Label(
            self.frame,
            text="UTC",
            font=(CLOCK_FONT, 12),
            fg="#888888",
            bg=BG_COLOR
        )
        self.offset_label.pack(pady=2)
    
    def update(self, time_str, date_str, offset_str):
        """Update the clock display"""
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        self.offset_label.config(text=offset_str)
    
    def get_frame(self):
        """Return the frame for packing"""
        return self.frame


class ControlPanel:
    """Control panel for managing timezones"""
    
    def __init__(self, parent, on_add_callback, on_remove_callback):
        self.parent = parent
        self.on_add_callback = on_add_callback
        self.on_remove_callback = on_remove_callback
        self.frame = tk.Frame(parent, bg="#2d2d44", height=80)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        self.frame.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create control panel widgets"""
        # Title
        title = tk.Label(
            self.frame,
            text="Timezone Manager",
            font=(CLOCK_FONT, 12, "bold"),
            fg=FG_COLOR,
            bg="#2d2d44"
        )
        title.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add button
        self.add_btn = tk.Button(
            self.frame,
            text="+ Add Timezone",
            command=self.on_add_callback,
            bg="#00b894",
            fg="#000000",
            font=(CLOCK_FONT, 10, "bold"),
            padx=15,
            pady=8
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        # Remove button
        self.remove_btn = tk.Button(
            self.frame,
            text="- Remove Timezone",
            command=self.on_remove_callback,
            bg="#ff6b6b",
            fg="#ffffff",
            font=(CLOCK_FONT, 10, "bold"),
            padx=15,
            pady=8
        )
        self.remove_btn.pack(side=tk.LEFT, padx=5)
    
    def get_frame(self):
        """Return the frame for packing"""
        return self.frame


class TimezoneSelector:
    """Dialog for selecting timezones"""
    
    def __init__(self, parent, available_timezones, callback):
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("Select Timezone")
        self.window.geometry("400x500")
        self.window.config(bg=BG_COLOR)
        
        # Search box
        search_frame = tk.Frame(self.window, bg=BG_COLOR)
        search_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(
            search_frame,
            text="Search:",
            fg=FG_COLOR,
            bg=BG_COLOR
        ).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=(CLOCK_FONT, 10),
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=10)
        
        # Listbox with scrollbar
        frame = tk.Frame(self.window, bg=BG_COLOR)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=(CLOCK_FONT, 10),
            bg="#2d2d44",
            fg=FG_COLOR,
            selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self._on_select)
        scrollbar.config(command=self.listbox.yview)
        
        # Store available timezones
        self.available_timezones = available_timezones
        self.filtered_timezones = available_timezones
        self._update_listbox()
        
        # Buttons
        btn_frame = tk.Frame(self.window, bg=BG_COLOR)
        btn_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="Select",
            command=self._on_select,
            bg="#00b894",
            fg="#000000",
            font=(CLOCK_FONT, 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.window.destroy,
            bg="#555555",
            fg=FG_COLOR,
            font=(CLOCK_FONT, 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
    
    def _on_search(self, *args):
        """Filter timezones based on search"""
        search_term = self.search_var.get().lower()
        self.filtered_timezones = [
            tz for tz in self.available_timezones 
            if search_term in tz.lower()
        ]
        self._update_listbox()
    
    def _update_listbox(self):
        """Update listbox with filtered timezones"""
        self.listbox.delete(0, tk.END)
        for tz in self.filtered_timezones:
            self.listbox.insert(tk.END, tz)
    
    def _on_select(self, event=None):
        """Handle timezone selection"""
        selection = self.listbox.curselection()
        if selection:
            selected_tz = self.filtered_timezones[selection[0]]
            self.callback(selected_tz)
            self.window.destroy()
