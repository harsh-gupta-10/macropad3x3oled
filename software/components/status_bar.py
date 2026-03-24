import tkinter as tk
import threading
import time
import os

class StatusBar:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app
        self.connected = False
        self.device_port = None
        self.stop_thread = False  # Flag to control the connection check thread

        status_frame = tk.Frame(self.root, bg="#0B1220", bd=1, relief="sunken", highlightbackground="#1E293B", highlightthickness=1)
        status_frame.place(x=10, y=450, width=920, height=40)

        # Left frame for User Action status
        self.user_action_frame = tk.Frame(status_frame, bg="#0B1220")
        self.user_action_frame.pack(side="left", fill="both", expand=True)
        self.user_action_label = tk.Label(self.user_action_frame, text="Status: Ready", bg="#0B1220", fg="#38BDF8", font=("Segoe UI", 10, "italic"))
        self.user_action_label.pack(side="left", padx=10)

        # Right frame for Connection Status
        self.connection_status_frame = tk.Frame(status_frame, bg="#0B1220")
        self.connection_status_frame.pack(side="right", fill="both", expand=True)
        self.connection_status_label = tk.Label(self.connection_status_frame, text="Connection Status: Disconnected", bg="#0B1220", fg="#EF4444", font=("Segoe UI", 10, "italic"))
        self.connection_status_label.pack(side="right", padx=10)
        
        # Start connection monitoring thread
        self.connection_thread = threading.Thread(target=self.check_connection_loop, daemon=True)
        self.connection_thread.start()
    
    def update_status(self, message):
        """Update the status bar with a message."""
        self.user_action_label.config(text=f"Status: {message}")
    
    def update_connection_status(self, connected, port=None):
        """Update the connection status display."""
        if connected:
            self.connection_status_label.config(text=f"Connection Status: Connected ({port})", fg="green")
            self.connected = True
            self.device_port = port
        else:
            self.connection_status_label.config(text="Connection Status: Disconnected", fg="red")
            self.connected = False
            self.device_port = None
    
    def check_connection(self):
        """Check if O: drive is mounted (device connected in mass-storage mode)."""
        try:
            if os.path.exists("O:\\"):
                self.root.after(0, lambda: self.update_connection_status(True, "O:"))
                return True

            self.root.after(0, lambda: self.update_connection_status(False))
            return False
        except Exception as e:
            print(f"Error checking drive connection: {e}")
            self.root.after(0, lambda: self.update_connection_status(False))
            return False
    
    def check_connection_loop(self):
        """Continuously check for device connection in a separate thread."""
        while not self.stop_thread:
            self.check_connection()
            time.sleep(2)  # Check every 2 seconds
    
    def stop(self):
        """Stop the connection checking thread when closing the application."""
        self.stop_thread = True
        if self.connection_thread.is_alive():
            self.connection_thread.join(timeout=1)