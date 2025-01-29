import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random

# Simulated Network Traffic Generator
def simulate_traffic():
    while True:
        time.sleep(1)
        network_traffic.append(random.randint(50, 200))

# DoS Attack Detection Logic
def detect_dos():
    threshold = 200
    window_size = 5

    while monitoring:
        if len(network_traffic) >= window_size:
            window_traffic = network_traffic[-window_size:]
            average_traffic = sum(window_traffic) / window_size
            if average_traffic > threshold:
                alert_user(average_traffic)
        time.sleep(1)

# Alert User about potential DoS attack
def alert_user(traffic):
    def show_alert():
        messagebox.showwarning("DoS Attack Detected", f"High traffic detected: {traffic:.2f} packets/sec\nPotential DoS attack in progress!")
    app.after(0, show_alert)

# Start Monitoring
def start_monitoring():
    global monitoring
    if not monitoring:
        monitoring = True
        threading.Thread(target=detect_dos, daemon=True).start()
        status_label.config(text="Status: Monitoring", fg="green")
        messagebox.showinfo("Monitoring", "DoS detection started.")

# Stop Monitoring
def stop_monitoring():
    global monitoring
    if monitoring:
        monitoring = False
        status_label.config(text="Status: Stopped", fg="red")
        messagebox.showinfo("Monitoring", "DoS detection stopped.")

# User Interface
app = tk.Tk()
app.title("DoS Attack Detection Tool")
app.geometry("400x300")

# Global Variables
network_traffic = []
monitoring = False

# Widgets
header = tk.Label(app, text="DoS Attack Detection Tool", font=("Helvetica", 16))
header.pack(pady=10)

status_label = tk.Label(app, text="Status: Stopped", font=("Helvetica", 12), fg="red")
status_label.pack(pady=5)

start_button = tk.Button(app, text="Start Monitoring", command=start_monitoring, bg="green", fg="white", font=("Helvetica", 12))
start_button.pack(pady=10)

stop_button = tk.Button(app, text="Stop Monitoring", command=stop_monitoring, bg="red", fg="white", font=("Helvetica", 12))
stop_button.pack(pady=10)

traffic_label = tk.Label(app, text="Network Traffic (packets/sec):", font=("Helvetica", 12))
traffic_label.pack(pady=5)

traffic_display = ttk.Treeview(app, columns=("time", "traffic"), show="headings", height=10)
traffic_display.heading("time", text="Time (s)")
traffic_display.heading("traffic", text="Traffic (packets/sec)")
traffic_display.column("time", width=100)
traffic_display.column("traffic", width=150)
traffic_display.pack(pady=10)

# Update traffic display
last_display_time = 0
def update_traffic_display():
    global last_display_time
    while True:
        if monitoring and network_traffic:
            for i, traffic in enumerate(network_traffic[last_display_time:], start=last_display_time):
                traffic_display.insert("", "end", values=(i + 1, traffic))
                last_display_time += 1
        time.sleep(1)

threading.Thread(target=simulate_traffic, daemon=True).start()
threading.Thread(target=update_traffic_display, daemon=True).start()

app.mainloop()
#end of dos.py