import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

# Countdown function
def start_timer():
    try:
        seconds = int(entry.get())
        if seconds <= 0:
            messagebox.showerror("Input Error", "Please enter a positive number.")
            return
        
        start_button.config(state=tk.DISABLED)  # Disable button during countdown
        entry.config(state=tk.DISABLED)
        countdown(seconds)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")

def countdown(seconds):
    def run():
        for i in range(seconds, 0, -1):
            timer_label.config(text=f"⏳ Time Left: {i} sec")
            time.sleep(1)

        timer_label.config(text="⏰ Time's Up!", foreground="red")
        messagebox.showinfo("Timer Alert", "Time's up!")  # Show alert

        # Re-enable UI elements
        entry.config(state=tk.NORMAL)
        start_button.config(state=tk.NORMAL)

    thread = threading.Thread(target=run)
    thread.start()

# GUI Setup
root = tk.Tk()
root.title("⏱ Countdown Timer")
root.geometry("350x250")
root.configure(bg="#f0f0f0")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

# Title Label
title_label = ttk.Label(root, text="⏱ Countdown Timer", font=("Arial", 16, "bold"), background="#f0f0f0")
title_label.pack(pady=10)

# Entry Box
entry_frame = ttk.Frame(root)
entry_frame.pack(pady=5)

entry = ttk.Entry(entry_frame, font=("Arial", 14), width=10, justify="center")
entry.pack(side=tk.LEFT, padx=5)

# Start Timer Button
start_button = ttk.Button(root, text="Start Timer", command=start_timer)
start_button.pack(pady=10)

# Timer Display
timer_label = ttk.Label(root, text="⏳ Enter time and press start", font=("Arial", 14, "bold"))
timer_label.pack(pady=10)

# Run GUI
root.mainloop()
