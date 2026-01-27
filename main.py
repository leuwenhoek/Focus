import tkinter as tk
from tkinter import messagebox
from AppOpener import open
from multiprocessing import process
import webbrowser

class AutoTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Persistent 8-Hour Timer")
        self.root.geometry("350x250")
        
        self.EIGHT_HOURS = 28800
        self.FIVE_MINS = 300
        
        self.remaining_seconds = self.EIGHT_HOURS
        self.is_paused = False
        
        self.status_label = tk.Label(root, text="Timer Running", fg="green", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)

        self.label = tk.Label(root, text=self.format_time(self.remaining_seconds), font=("Helvetica", 45))
        self.label.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop (Pause 5m)", command=self.handle_stop, 
                                     bg="#ff4444", fg="white", width=20, height=2)
        self.stop_button.pack(pady=10)

        self.update_timer()

    def format_time(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        if not self.is_paused and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.label.config(text=self.format_time(self.remaining_seconds))
            self.root.after(1000, self.update_timer)
        elif self.remaining_seconds <= 0:
            messagebox.showinfo("Done", "8 Hours Completed!")

    def handle_stop(self):
        if self.is_paused:
            return 
            
        self.is_paused = True
        self.status_label.config(text="PAUSED: Resuming in 5 mins", fg="red")
        self.stop_button.config(state="disabled")
        
        self.root.after(300000, self.resume_timer)

    def resume_timer(self):
        self.is_paused = False
        self.status_label.config(text="Timer Running", fg="green")
        self.stop_button.config(state="normal")
        self.update_timer()

def timer():
    root = tk.Tk()
    app = AutoTimer(root)
    root.mainloop()

    
