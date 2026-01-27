import pygetwindow as gw
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser
import winsound  
import os
import multiprocessing
from AppOpener import open as open_app
import subprocess
import psutil
import pyautogui

WARNING_VIDEO_URL = "https://www.youtube.com/watch?v=jcVAScA36g4"

class persistentTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer & Search")
        self.root.geometry("400x400")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.remaining_seconds = self.load_time()
        self.is_paused = False
        
        self.status_label = tk.Label(root, text="Timer Running", fg="green", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)

        self.label = tk.Label(root, text=self.format_time(), font=("Helvetica", 40))
        self.label.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop (Pause 5m)", command=self.handle_stop, 
                                     bg="#ff4444", fg="white", width=15)
        self.stop_button.pack(pady=5)

        tk.Label(root, text="Search Box:", font=("Arial", 10)).pack(pady=(20, 0))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var, width=30, font=("Arial", 12))
        self.search_entry.pack(pady=5)
        
        self.search_entry.bind('<Return>', lambda event: self.execute_search())

        self.search_button = tk.Button(root, text="Search", command=self.execute_search)
        self.search_button.pack(pady=5)

        self.update_timer()

    def load_time(self):
        return 28800

    def on_closing(self):
        """Action when user tries to close the window"""
        winsound.Beep(1000, 2000) 
        messagebox.showwarning("Access Denied", "You cannot close this timer!")

    def format_time(self):
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def update_timer(self):
        if not self.is_paused and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.label.config(text=self.format_time())
            self.root.after(1000, self.update_timer)

    def handle_stop(self):
        if not self.is_paused:
            self.is_paused = True
            self.status_label.config(text="PAUSED: Resuming in 5 mins", fg="red")
            self.root.after(300000, self.resume_timer)

    def resume_timer(self):
        self.is_paused = False
        self.status_label.config(text="Timer Running", fg="green")
        self.update_timer()

    def execute_search(self):
        query = self.search_var.get()
        after_url = query.replace(" ", "+")
        url = f'https://youtube.com/results?search_query={after_url}'
        webbrowser.open_new_tab(url)
        self.search_entry.delete(0, tk.END)

def GUI_activation():
    root = tk.Tk()
    app = persistentTimerApp(root)
    root.mainloop()

def open_warning_video():
    """Helper to open the specific warning link"""
    webbrowser.open(WARNING_VIDEO_URL)

def monitor_brave_tabs():
    print("Monitoring Brave Tabs and closing unwanted tabs...")
    try:
        while True:
            violation_detected = False
            brave_windows = gw.getWindowsWithTitle('Brave')
            
            for window in brave_windows:
                title = window.title
                if " - Brave" in title:
                    clean_name = title.replace(" - Brave", "").strip()
                    is_allowed = any(word in clean_name.lower() for word in ["youtube", "gemini", "new tab", "untitled"])
                    
                    if not is_allowed:
                        print(f"Closing disallowed tab: {clean_name}")
                        violation_detected = True
                        try:
                            window.activate()
                            time.sleep(0.3)
                            pyautogui.hotkey('ctrl', 'w')
                            time.sleep(0.5)
                        except Exception as e:
                            print(f"Error closing tab: {e}")
            
            blocked_apps = ['chrome', 'notepad', 'slack', 'task manager']
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(blocked_app in proc_name for blocked_app in blocked_apps):
                        print(f"Closing disallowed application: {proc.info['name']}")
                        violation_detected = True
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if violation_detected:
                open_warning_video()
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    open_app('Brave')
    p1 = multiprocessing.Process(target=GUI_activation)
    p2 = multiprocessing.Process(target=monitor_brave_tabs)
    p1.start()
    p2.start()
    p1.join()
    p2.join()