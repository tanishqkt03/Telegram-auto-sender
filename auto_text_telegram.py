import time
import asyncio
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime, timezone
from telethon.sync import TelegramClient
import threading
import os
import sys

# Your Telegram credentials
API_ID = 0  # Your API ID
API_HASH = ""  # Your API Hash
TARGET_USER = 0  # Can be a username, phone number, or chat ID

# Create Telethon client
client = TelegramClient("session_name", API_ID, API_HASH)

# Global stop flag
stop_flag = False

# Function to send a message asynchronously
async def send_message(text):
    async with client:
        await client.send_message(TARGET_USER, text)
        update_status(f"✅ Message sent at {datetime.now().strftime('%H:%M:%S.%f')}")
        messagebox.showinfo("Success", f"Message sent at {datetime.now().strftime('%H:%M:%S.%f')}")
        time.sleep(7)#sleep 7 s then reset
        reset_program()

# Function to safely send message inside its own event loop
def send_message_thread_safe(message):
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set this new loop as the current loop
    loop.run_until_complete(send_message(message))  # Run the async function
    loop.close()  # Close the loop after execution

# Function to schedule message at exact time (LOCAL TIME) using milliseconds
def precise_send(target_hour, target_minute, target_second, message):
    global stop_flag
    target_time_ms = (target_hour * 3600 + target_minute * 60 + target_second) * 1000  # Convert to milliseconds

    while True:
        if stop_flag:  
            update_status("❌ Process Stopped.")
            return  # Exit if stopped

        now = datetime.now(timezone.utc).astimezone()  # Get local time
        current_time_ms = (now.hour * 3600 + now.minute * 60 + now.second) * 1000 + now.microsecond // 1000  # Convert to ms
        remaining_time_ms = target_time_ms - current_time_ms  # Remaining time in ms

        update_status(f"⌛ Current Time: {now.strftime('%H:%M:%S.%f')} | Remaining: {remaining_time_ms:.3f} ms")

        if 0< remaining_time_ms <= 1000:  # Send message when 0.5ms before target
            threading.Thread(target=send_message_thread_safe, args=(message,), daemon=True).start()  # Run async safely
            break  # Exit after sending

        if remaining_time_ms < 0:
            messagebox.showerror("Error", "❌ The target time has already passed!")
            update_status("❌ Error: Target time already passed.")
            break

        time.sleep(0.0005)  # Check time every 0.5ms (500µs) for ultra-precision

# Function to update status in the GUI
def update_status(message):
    status_box.config(state=tk.NORMAL)
    status_box.insert(tk.END, message + "\n")
    status_box.see(tk.END)  # Auto-scroll to latest message
    status_box.config(state=tk.DISABLED)

# Function to get user input and start the script
def start_sending():
    global stop_flag
    stop_flag = False  # Reset stop flag

    try:
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())
        second = int(second_entry.get())
        message = message_entry.get("1.0", "end-1c")  # Get text from Tkinter Text widget

        if not message.strip():  # Ensure message isn't empty after stripping spaces
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        update_status(f"🚀 Scheduled to send at {hour}:{minute}:{second}.")

        # Run precise_send in a separate thread to keep GUI responsive
        threading.Thread(target=precise_send, args=(hour, minute, second, message), daemon=True).start()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

# Function to stop the process
def stop_sending():
    global stop_flag
    stop_flag = True  # Set stop flag to terminate the loop

# Function to reset the program
def reset_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)  # Restart the program

# Create GUI
root = tk.Tk()
root.title("Telegram Auto-Sender")
root.geometry("500x500")  # Increased window size
root.resizable(True, True)  # Allows resizing

# Labels and input fields
tk.Label(root, text="Enter Target Time (HH:MM:SS)").pack(pady=5)

frame = tk.Frame(root)
frame.pack()
hour_entry = tk.Entry(frame, width=5)
hour_entry.pack(side=tk.LEFT, padx=2)
tk.Label(frame, text=":").pack(side=tk.LEFT)
minute_entry = tk.Entry(frame, width=5)
minute_entry.pack(side=tk.LEFT, padx=2)
tk.Label(frame, text=":").pack(side=tk.LEFT)
second_entry = tk.Entry(frame, width=5)
second_entry.pack(side=tk.LEFT, padx=2)

tk.Label(root, text="Enter Message").pack(pady=5)
message_entry = tk.Text(root, height=3, width=50)  # Increased size for easier input
message_entry.pack()

# Start, Stop, and Reset buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", command=start_sending, bg="green", fg="white", width=12)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_sending, bg="red", fg="white", width=12)
stop_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_program, bg="blue", fg="white", width=12)
reset_button.pack(side=tk.LEFT, padx=5)

# Status box for live updates (Larger and scrollable)
tk.Label(root, text="Status:").pack(pady=5)
status_box = scrolledtext.ScrolledText(root, height=12, width=60, state=tk.DISABLED)  # Increased size
status_box.pack(expand=True, fill="both")  # Allows resizing

# Run the GUI
root.mainloop()
