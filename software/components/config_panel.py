import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from engine import update_profile_key, load_special_keys, update_special_key, load_settings, update_settings
import os

class ConfigPanel:
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app  # Reference to main app
        self.special_action_options = {
            "Volume Encoder - Left Rotation": "volume_encoder_left",
            "Volume Encoder - Right Rotation": "volume_encoder_right",
            "Volume Encoder - Click": "volume_encoder_click",
            "Volume Encoder - Hold": "volume_encoder_hold",
            "Display Encoder - Left Rotation": "display_encoder_left",
            "Display Encoder - Right Rotation": "display_encoder_right",
            "Display Encoder - Click": "display_encoder_click",
            "Display Encoder - Hold": "display_encoder_hold",
            "Mic Key (Fixed Button)": "mic_key",
        }
        self.create_ui()

    def create_ui(self):
        """Create the key changer panel."""
        self.parent.option_add("*Font", "{Segoe UI} 10")
        self.parent.option_add("*TCombobox*Listbox.background", "#0B1220")
        self.parent.option_add("*TCombobox*Listbox.foreground", "#E2E8F0")
        self.parent.option_add("*TCombobox*Listbox.selectBackground", "#0EA5E9")
        self.parent.option_add("*TCombobox*Listbox.selectForeground", "#082F49")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("App.TNotebook", background="#0F172A", borderwidth=0)
        style.configure("App.TNotebook.Tab", background="#1E293B", foreground="#E2E8F0", padding=(6, 7), font=("Segoe UI", 9, "bold"))
        style.map(
            "App.TNotebook.Tab",
            background=[("selected", "#0EA5E9")],
            foreground=[("selected", "#082F49")],
        )
        style.configure("App.TCombobox", fieldbackground="#0B1220", background="#0B1220", foreground="#E2E8F0", arrowcolor="#E2E8F0", bordercolor="#334155", lightcolor="#334155", darkcolor="#334155")
        style.map(
            "App.TCombobox",
            fieldbackground=[("readonly", "#0B1220")],
            foreground=[("readonly", "#E2E8F0")],
            selectforeground=[("readonly", "#E2E8F0")],
            selectbackground=[("readonly", "#0B1220")],
        )

        config_frame = tk.Frame(self.parent, bg="#111827", bd=1, relief="ridge", highlightbackground="#1F2937", highlightthickness=1)
        config_frame.place(x=540, y=10, width=390, height=430)

        tk.Label(config_frame, text="Key Changer Panel", bg="#111827", fg="#F8FAFC", font=("Segoe UI", 13, "bold"), pady=6).pack()

        self.tab_control = ttk.Notebook(config_frame, style="App.TNotebook")  # Save as instance variable
        self.tab_control.pack(expand=1, fill="both")

        # Tab for Basic Configuration
        basic_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(basic_tab, text="Basic Config")

        # Name Input Box at the top
        self.text_box_label = tk.Label(basic_tab, text="Name(Use):", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 11, "bold"))
        self.text_box_label.pack(pady=5)

        self.text_box = tk.Text(basic_tab, height=1.2, width=30, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.text_box.pack(pady=5)

        # Category Dropdown (First Dropdown)
        tk.Label(basic_tab, text="Select Category", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=5)
        self.key_category_var = tk.StringVar()
        self.key_category_var.set("Alphabets")  # Default Category

        category_dropdown = ttk.Combobox(basic_tab, textvariable=self.key_category_var, state="readonly", style="App.TCombobox")
        category_dropdown["values"] = ["Alphabets", "Numbers", "Symbols", "F1-F24", "Navigation Keys", 
                                       "Modifiers", "System Keys", "Media Keys", "Numpad Keys", "Other Keys"]
        category_dropdown.pack(pady=5)
        
        # Specific Keys Dropdown (Second Dropdown)
        tk.Label(basic_tab, text="Select Key", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=5)
        self.specific_keys_var = tk.StringVar()
        self.specific_keys_dropdown = ttk.Combobox(basic_tab, textvariable=self.specific_keys_var, state="readonly", style="App.TCombobox")
        self.specific_keys_dropdown.pack(pady=5)

        # Update the second dropdown based on the selected category
        self.update_specific_keys()
        category_dropdown.bind("<<ComboboxSelected>>", self.update_specific_keys)

        # Save Button
        save_button = tk.Button(basic_tab, text="Save", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_config)
        save_button.pack(pady=10)

        # Tab for Advanced Configuration
        advanced_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(advanced_tab, text="Advanced")

        # Create inner scrollable frame
        advanced_scroll_frame = tk.Frame(advanced_tab, bg="#0F172A")
        advanced_scroll_frame.pack(side="top", fill="x", expand=False, pady=5)

        # Name input box at the top
        self.advanced_text_label = tk.Label(advanced_scroll_frame, text="Name(Use):", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 11, "bold"))
        self.advanced_text_label.pack(pady=5)

        self.advanced_text_box = tk.Text(advanced_scroll_frame, height=1.2, width=30, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.advanced_text_box.pack(pady=10)

        # Radio buttons for key combination options
        self.key_combo_var = tk.IntVar(value=2)
        radio_frame = tk.Frame(advanced_scroll_frame, bg="#0F172A")
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="2 Keys", variable=self.key_combo_var, value=2, 
                      bg="#0F172A", fg="#E2E8F0", selectcolor="#0B1220", 
                      command=self.update_key_dropdowns).pack(side="left", padx=20)
        tk.Radiobutton(radio_frame, text="3 Keys", variable=self.key_combo_var, value=3, 
                      bg="#0F172A", fg="#E2E8F0", selectcolor="#0B1220",
                      command=self.update_key_dropdowns).pack(side="left", padx=20)

        # Frame for Dropdowns (doesn't expand vertically)
        self.dropdown_frame = tk.Frame(advanced_scroll_frame, bg="#0F172A")
        self.dropdown_frame.pack(pady=10, fill="none", expand=False)

        # First modifier dropdown
        self.first_modifier_label = tk.Label(self.dropdown_frame, text="First Modifier:", bg="#0F172A", fg="#E2E8F0")
        self.first_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_1 = ttk.Combobox(
            self.dropdown_frame, textvariable=self.first_modifier_var, state="readonly",
            values=["None", "Ctrl", "Alt", "Shift","windows"], style="App.TCombobox"
        )

        # Second modifier dropdown (can't match first)
        self.second_modifier_label = tk.Label(self.dropdown_frame, text="Second Modifier:", bg="#0F172A", fg="#E2E8F0")
        self.second_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_2 = ttk.Combobox(
            self.dropdown_frame, textvariable=self.second_modifier_var, state="readonly",
            values=["None", "Ctrl", "Alt", "Shift","windows"], style="App.TCombobox"
        )

        # Third dropdown (all keys)
        self.third_key_label = tk.Label(self.dropdown_frame, text="Key:", bg="#0F172A", fg="#E2E8F0")
        self.third_key_var = tk.StringVar()
        all_keys = (
            [chr(i) for i in range(65, 91)] +  # A-Z
            [str(i) for i in range(10)] +      # 0-9
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{",
             "}", "[", "]", "|", "\\", ":", ";", '"', "'", "<", ">", ",", ".", "?", "/"] +
            [f"F{i}" for i in range(1, 25)] +  # F1-F24
            ["Up", "Down", "Left", "Right", "Home", "End", "Page Up", "Page Down"] +  # Navigation
            ["Shift", "Ctrl", "Alt", "Caps Lock", "Tab"] +  # Modifiers
            ["Insert", "Delete", "Print Screen", "Scroll Lock", "Pause/Break"] +  # System Keys
            ["Volume Up", "Volume Down", "Mute", "Play/Pause", "Stop", "Next Track", "Previous Track"] +  # Media Keys
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] +  # Numpad Numbers
            ["+", "-", "*", "/", "Enter", "Decimal"] +  # Numpad Operators
            ["Escape", "Space", "Backspace"] +  # Other Keys
            ["windows"]  # Add more keys as needed
        )
        self.third_dropdown = ttk.Combobox(
            self.dropdown_frame, textvariable=self.third_key_var, state="readonly",
            values=all_keys, style="App.TCombobox"
        )

        self.modifier_dropdown_1.bind("<<ComboboxSelected>>", self.sync_modifiers)
        self.modifier_dropdown_2.bind("<<ComboboxSelected>>", self.sync_modifiers)

        # Initialize dropdowns based on default radio selection
        self.update_key_dropdowns()

        # Save Button (pinned at bottom)
        advanced_save_button = tk.Button(advanced_tab, text="Save", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_config)
        advanced_save_button.pack(side="bottom", pady=10)

        # Tab for Software Configuration
        software_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(software_tab, text="Software")

        # Name input box at the top
        self.software_text_label = tk.Label(software_tab, text="Name(Use):", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 11, "bold"))
        self.software_text_label.pack(pady=5)

        self.software_text_box = tk.Text(software_tab, height=1.2, width=30, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.software_text_box.pack(pady=10)

        # Software selection dropdown
        tk.Label(software_tab, text="Select Software:", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=5)
        self.software_var = tk.StringVar(value="notepad")
        common_software = [
            "notepad", "mspaint", "calc", "explorer", 
            "chrome", "firefox", "msedge", "vscode",
            "word", "excel", "powerpoint", "outlook",
            "discord", "spotify", "photoshop", "blender",
            "steam", "obs", "vlc", "cmd"
        ]
        
        self.software_dropdown = ttk.Combobox(software_tab, textvariable=self.software_var, state="readonly", values=common_software, style="App.TCombobox")
        self.software_dropdown.pack(pady=5)
        
        # Custom software path option
        custom_frame = tk.Frame(software_tab, bg="#0F172A")
        custom_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(custom_frame, text="Or Enter your Software name:", bg="#0F172A", fg="#E2E8F0").pack(anchor="w")
        
        path_frame = tk.Frame(custom_frame, bg="#0F172A")
        path_frame.pack(fill="x", pady=5)
        
        self.custom_path_var = tk.StringVar()
        self.custom_path_entry = tk.Entry(path_frame, textvariable=self.custom_path_var, bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", relief="flat")
        self.custom_path_entry.pack(side="left", expand=True, fill="x", padx=(0,5))
        
        
        
        # Modifier key option (for software launch with hotkey)
        modifier_frame = tk.Frame(software_tab, bg="#0F172A")
        modifier_frame.pack(pady=10)
        
        tk.Label(modifier_frame, text="Type:", bg="#0F172A", fg="#E2E8F0").pack(side="left", padx=5)
        
        self.software_modifier_var = tk.StringVar(value="Software")
        ttk.Combobox(
            modifier_frame, textvariable=self.software_modifier_var, state="readonly",
            values=["Software"], width=10, style="App.TCombobox"
        ).pack(side="left", padx=5)
        
        # Save Button
        software_save_button = tk.Button(software_tab, text="Save", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_config)
        software_save_button.pack(pady=10)

        # Tab for Text/Paragraph typing
        text_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(text_tab, text="Text/Para")

        tk.Label(text_tab, text="Name(Use):", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 11, "bold")).pack(pady=(8, 4))
        self.textpara_name_box = tk.Text(text_tab, height=1.2, width=30, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.textpara_name_box.pack(pady=(0, 8))

        tk.Label(text_tab, text="Text to Type:", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=(2, 4))
        self.textpara_content_box = tk.Text(text_tab, height=7, width=32, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.textpara_content_box.pack(pady=(0, 8), padx=12)

        type_row = tk.Frame(text_tab, bg="#0F172A")
        type_row.pack(pady=(0, 6))
        tk.Label(type_row, text="Typing Style:", bg="#0F172A", fg="#E2E8F0").pack(side="left", padx=(0, 6))
        self.text_type_var = tk.StringVar(value="single")
        ttk.Combobox(
            type_row,
            textvariable=self.text_type_var,
            state="readonly",
            values=["single", "line-by-line", "paragraph"],
            width=14,
            style="App.TCombobox",
        ).pack(side="left")

        self.text_enter_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            text_tab,
            text="Press Enter after typing",
            variable=self.text_enter_var,
            bg="#0F172A",
            fg="#E2E8F0",
            selectcolor="#0B1220",
            activebackground="#0F172A",
            activeforeground="#E2E8F0",
        ).pack(pady=(0, 4))

        self.text_shift_enter_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            text_tab,
            text="Use Shift+Enter for new line",
            variable=self.text_shift_enter_var,
            bg="#0F172A",
            fg="#E2E8F0",
            selectcolor="#0B1220",
            activebackground="#0F172A",
            activeforeground="#E2E8F0",
        ).pack(pady=(0, 8))

        text_save_button = tk.Button(text_tab, text="Save", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_config)
        text_save_button.pack(pady=(0, 8))

        # Tab for Special Keys Configuration
        special_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(special_tab, text="Special Keys")

        tk.Label(special_tab, text="Special Action", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=(8, 4))
        self.special_action_var = tk.StringVar(value=list(self.special_action_options.keys())[0])
        self.special_action_dropdown = ttk.Combobox(
            special_tab,
            textvariable=self.special_action_var,
            state="readonly",
            values=list(self.special_action_options.keys()),
            style="App.TCombobox",
        )
        self.special_action_dropdown.pack(pady=4)

        tk.Label(special_tab, text="Name(Use):", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10, "bold")).pack(pady=(8, 4))
        self.special_name_box = tk.Text(special_tab, height=1.2, width=30, wrap="word", bg="#0B1220", fg="#E2E8F0", insertbackground="#E2E8F0", font=("Segoe UI", 10), relief="flat")
        self.special_name_box.pack(pady=4)

        self.special_mode_var = tk.StringVar(value="Keyboard Combo")
        mode_frame = tk.Frame(special_tab, bg="#0F172A")
        mode_frame.pack(pady=8)
        tk.Label(mode_frame, text="Output Type:", bg="#0F172A", fg="#E2E8F0").pack(side="left", padx=4)
        self.special_mode_dropdown = ttk.Combobox(
            mode_frame,
            textvariable=self.special_mode_var,
            state="readonly",
            values=["Keyboard Combo", "Internal Action"],
            width=16,
            style="App.TCombobox",
        )
        self.special_mode_dropdown.pack(side="left", padx=4)

        self.special_keyboard_frame = tk.Frame(special_tab, bg="#0F172A")
        self.special_keyboard_frame.pack(pady=4)

        self.special_mod1_var = tk.StringVar(value="None")
        self.special_mod2_var = tk.StringVar(value="None")
        self.special_key_var = tk.StringVar(value="A")

        ttk.Combobox(self.special_keyboard_frame, textvariable=self.special_mod1_var, state="readonly", values=["None", "Ctrl", "Alt", "Shift", "windows"], width=10, style="App.TCombobox").pack(pady=2)
        ttk.Combobox(self.special_keyboard_frame, textvariable=self.special_mod2_var, state="readonly", values=["None", "Ctrl", "Alt", "Shift", "windows"], width=10, style="App.TCombobox").pack(pady=2)
        ttk.Combobox(self.special_keyboard_frame, textvariable=self.special_key_var, state="readonly", values=all_keys + ["media_volume_up", "media_volume_down", "media_mute", "media_play_pause"], width=22, style="App.TCombobox").pack(pady=2)

        self.special_internal_frame = tk.Frame(special_tab, bg="#0F172A")
        self.special_internal_action_var = tk.StringVar(value="none")
        tk.Label(self.special_internal_frame, text="Internal Action:", bg="#0F172A", fg="#E2E8F0").pack(pady=(2, 4))
        ttk.Combobox(
            self.special_internal_frame,
            textvariable=self.special_internal_action_var,
            state="readonly",
            values=["none", "profile_prev", "profile_next"],
            width=20,
            style="App.TCombobox",
        ).pack(pady=2)

        special_btn_row = tk.Frame(special_tab, bg="#0F172A")
        special_btn_row.pack(pady=8)
        tk.Button(special_btn_row, text="Load Action", bg="#334155", fg="#E2E8F0", relief="flat", command=self.load_special_config).pack(side="left", padx=6)
        tk.Button(special_btn_row, text="Save", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_special_config).pack(side="left", padx=6)

        self.special_action_dropdown.bind("<<ComboboxSelected>>", self.load_special_config)
        self.special_mode_dropdown.bind("<<ComboboxSelected>>", self.toggle_special_mode)
        self.toggle_special_mode()
        self.load_special_config()

        # Tab for Settings Configuration
        settings_tab = tk.Frame(self.tab_control, bg="#0F172A")
        self.tab_control.add(settings_tab, text="Settings")

        # Encoder Speed Configuration
        encoder_frame = tk.Frame(settings_tab, bg="#0F172A")
        encoder_frame.pack(pady=15, padx=10, fill="x")

        tk.Label(encoder_frame, text="Encoder Speed Settings:", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 11, "bold")).pack(pady=(0, 10))

        # Volume Encoder Speed
        volume_row = tk.Frame(encoder_frame, bg="#0F172A")
        volume_row.pack(pady=8, fill="x")
        
        tk.Label(volume_row, text="Volume Encoder Speed:", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10)).pack(side="left", padx=(0, 10))
        
        self.volume_speed_var = tk.IntVar(value=3)
        
        tk.Button(volume_row, text="−", bg="#334155", fg="#E2E8F0", width=3, relief="flat", command=lambda: self.adjust_volume_speed(-1)).pack(side="left", padx=2)
        volume_spinbox = tk.Spinbox(
            volume_row, 
            from_=1, 
            to=5, 
            textvariable=self.volume_speed_var,
            width=5,
            bg="#0B1220",
            fg="#E2E8F0",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        volume_spinbox.pack(side="left", padx=2)
        tk.Button(volume_row, text="+", bg="#334155", fg="#E2E8F0", width=3, relief="flat", command=lambda: self.adjust_volume_speed(1)).pack(side="left", padx=2)
        
        self.volume_speed_label = tk.Label(volume_row, text="(Slower → Faster)", bg="#0F172A", fg="#96D1FF", font=("Segoe UI", 9, "italic"))
        self.volume_speed_label.pack(side="left", padx=10)

        # Display Encoder Speed
        display_row = tk.Frame(encoder_frame, bg="#0F172A")
        display_row.pack(pady=8, fill="x")
        
        tk.Label(display_row, text="Display Encoder Speed:", bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10)).pack(side="left", padx=(0, 10))
        
        self.display_speed_var = tk.IntVar(value=1)
        
        tk.Button(display_row, text="−", bg="#334155", fg="#E2E8F0", width=3, relief="flat", command=lambda: self.adjust_display_speed(-1)).pack(side="left", padx=2)
        display_spinbox = tk.Spinbox(
            display_row, 
            from_=1, 
            to=5, 
            textvariable=self.display_speed_var,
            width=5,
            bg="#0B1220",
            fg="#E2E8F0",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        display_spinbox.pack(side="left", padx=2)
        tk.Button(display_row, text="+", bg="#334155", fg="#E2E8F0", width=3, relief="flat", command=lambda: self.adjust_display_speed(1)).pack(side="left", padx=2)
        
        self.display_speed_label = tk.Label(display_row, text="(Slower → Faster)", bg="#0F172A", fg="#96D1FF", font=("Segoe UI", 9, "italic"))
        self.display_speed_label.pack(side="left", padx=10)

        # Load current settings
        self.load_settings_ui()

        # Save Button for Settings
        settings_save_button = tk.Button(settings_tab, text="Save Settings", bg="#0EA5E9", fg="#082F49", font=("Segoe UI", 10, "bold"), relief="flat", command=self.save_settings)
        settings_save_button.pack(pady=15)

    def adjust_volume_speed(self, delta):
        """Adjust volume speed with bounds checking"""
        current = self.volume_speed_var.get()
        new_value = current + delta
        if 1 <= new_value <= 5:
            self.volume_speed_var.set(new_value)

    def adjust_display_speed(self, delta):
        """Adjust display speed with bounds checking"""
        current = self.display_speed_var.get()
        new_value = current + delta
        if 1 <= new_value <= 5:
            self.display_speed_var.set(new_value)

    def load_settings_ui(self):
        """Load settings from JSON and populate UI"""
        try:
            settings = load_settings()
            encoder_speeds = settings.get("encoder_speeds", {})
            
            self.volume_speed_var.set(encoder_speeds.get("volume", 3))
            self.display_speed_var.set(encoder_speeds.get("display", 1))
        except Exception as e:
            print(f"Error loading settings UI: {e}")

    def save_settings(self):
        """Save settings to JSON"""
        try:
            volume_speed = self.volume_speed_var.get()
            display_speed = self.display_speed_var.get()
            
            update_settings("encoder_speeds.volume", volume_speed)
            update_settings("encoder_speeds.display", display_speed)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {e}")

    def update_specific_keys(self, event=None):
        """Update the specific keys dropdown based on the selected category."""
        category = self.key_category_var.get()
        if category == "Alphabets":
            keys = [chr(i) for i in range(65, 91)]  # A-Z
        elif category == "Numbers":
            keys = [str(i) for i in range(10)]
        elif category == "Symbols":
            keys = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{", 
                   "}", "[", "]", "|", "\\", ":", ";", '"', "'", "<", ">", ",", ".", "?", "/"]
        elif category == "F1-F24":
            keys = [f"F{i}" for i in range(1, 25)]
        elif category == "Navigation Keys":
            keys = ["Up", "Down", "Left", "Right", "Home", "End", "Page Up", "Page Down"]
        elif category == "Modifiers":
            keys = ["Shift", "Ctrl", "Alt", "Caps Lock", "Tab"]
        elif category == "System Keys":
            keys = ["Insert", "Delete", "Print Screen", "Scroll Lock", "Pause/Break"]
        elif category == "Media Keys":
            keys = ["Volume Up", "Volume Down", "Mute", "Play/Pause", "Stop", "Next Track", "Previous Track"]
        elif category == "Numpad Keys":
            keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "Enter", "Decimal"]
        elif category == "Other Keys":
            keys = ["Escape", "Space", "Backspace", "windows"]
        else:
            keys = []
        self.specific_keys_dropdown["values"] = keys
        if keys:
            self.specific_keys_var.set(keys[0])
        else:
            self.specific_keys_var.set("")

    def save_config(self):
        """Collect user input and update the key configuration."""
        # Get the currently selected profile and key
        if not hasattr(self.app, 'selected_profile') or not hasattr(self.app, 'selected_key'):
            messagebox.showwarning("Selection Required", "Please select a profile and key first.")
            return
            
        profile_index = self.app.selected_profile
        key_index = self.app.selected_key
        
        # Get configuration from the active tab
        active_tab = self.tab_control.index("current")  # Get the current tab index
        
        text_content = None
        text_type = "single"
        text_press_enter = None

        if active_tab == 0:  # Basic tab
            specific_key = self.specific_keys_var.get()
            name = self.text_box.get("1.0", "end-1c").strip()
            key_combination = [specific_key.lower()]
            software = None
            extra_data = {
                "action": "key_combo",
                "software": None,
                "text_content": None,
                "text_type": None,
                "text_press_enter": None,
            }
        elif active_tab == 1:  # Advanced tab
            num_keys = self.key_combo_var.get()
            name = self.advanced_text_box.get("1.0", "end-1c").strip()
            software = None
            extra_data = {
                "action": "key_combo",
                "software": None,
                "text_content": None,
                "text_type": None,
                "text_press_enter": None,
            }
            
            if num_keys == 2:
                # 2-key combination
                modifiers = []
                if self.first_modifier_var.get() != "None":
                    modifiers.append(self.first_modifier_var.get().lower())
                    
                main_key = self.third_key_var.get().lower()
                key_combination = modifiers + [main_key]
            else:
                # 3-key combination
                modifiers = []
                if self.first_modifier_var.get() != "None":
                    modifiers.append(self.first_modifier_var.get().lower())
                if self.second_modifier_var.get() != "None":
                    modifiers.append(self.second_modifier_var.get().lower())
                    
                main_key = self.third_key_var.get().lower()
                key_combination = modifiers + [main_key]
        elif active_tab == 2:  # Software tab
            name = self.software_text_box.get("1.0", "end-1c").strip()
            # Use custom path if provided, otherwise use selected software
            if self.custom_path_var.get().strip():
                software = self.custom_path_var.get().strip()
            else:
                software = self.software_var.get()
                
            # Add modifier key if selected
            if self.software_modifier_var.get() != "None":
                key_combination = [self.software_modifier_var.get().lower()]
            else:
                key_combination = []
            extra_data = {
                "action": "software",
                "software": software,
                "text_content": None,
                "text_type": None,
                "text_press_enter": None,
            }
        elif active_tab == 3:  # Text/Para tab
            name = self.textpara_name_box.get("1.0", "end-1c").strip()
            software = None
            key_combination = ["text_input"]
            text_content = self.textpara_content_box.get("1.0", "end-1c")
            text_type = self.text_type_var.get()
            text_press_enter = bool(self.text_enter_var.get())
            text_shift_enter = bool(self.text_shift_enter_var.get())
            extra_data = {
                "action": "text_input",
                "software": None,
                "text_content": text_content,
                "text_type": text_type,
                "text_press_enter": text_press_enter,
                "text_shift_enter": text_shift_enter,
            }

            if not text_content.strip():
                messagebox.showwarning("Missing Text", "Please enter text to type.")
                return
        else:
            messagebox.showwarning("Unsupported Tab", "Please use Basic, Advanced, Software, or Text/Para tab to save key configuration.")
            return
        
        # Ensure extra fields are cleaned up when switching action types.
        if name == "":
            name = f"Key {key_index}"
        
        # Update the key configuration
        if update_profile_key(profile_index, key_index, key_combination, name, extra_data):
            messagebox.showinfo("Success", f"Key {key_index} updated in profile {profile_index}")
            
            # Update UI to show the new configuration
            if hasattr(self.app, 'refresh_keypad'):
                self.app.refresh_keypad()
        else:
            messagebox.showerror("Error", "Failed to update key configuration")

    def _normalize_key_token(self, key_text):
        """Normalize UI key labels to firmware token format."""
        token = key_text.strip().lower().replace(" ", "_")
        token = token.replace("/", "_").replace("-", "_")
        if token == "escape":
            return "esc"
        if token == "print_screen":
            return "print_screen"
        return token

    def _to_ui_key_label(self, token):
        """Convert stored token to a display label present in dropdown values."""
        if token.startswith("f") and token[1:].isdigit():
            return token.upper()
        labels = {
            "esc": "Escape",
            "page_up": "Page Up",
            "page_down": "Page Down",
            "print_screen": "Print Screen",
            "media_volume_up": "media_volume_up",
            "media_volume_down": "media_volume_down",
            "media_mute": "media_mute",
            "media_play_pause": "media_play_pause",
        }
        return labels.get(token, token.upper() if len(token) == 1 and token.isalpha() else token)

    def toggle_special_mode(self, event=None):
        """Switch between keyboard combo and internal action editing."""
        if self.special_mode_var.get() == "Internal Action":
            self.special_keyboard_frame.pack_forget()
            self.special_internal_frame.pack(pady=4)
        else:
            self.special_internal_frame.pack_forget()
            self.special_keyboard_frame.pack(pady=4)

    def load_special_config(self, event=None):
        """Load selected special key action from special-keyout.json."""
        special_data = load_special_keys()
        action_label = self.special_action_var.get()
        action_id = self.special_action_options.get(action_label)
        if not action_id:
            return

        action_data = special_data.get(action_id, {})
        action_name = action_data.get("name", action_label)
        self.special_name_box.delete("1.0", "end")
        self.special_name_box.insert("1.0", action_name)

        if "action" in action_data:
            self.special_mode_var.set("Internal Action")
            self.special_internal_action_var.set(action_data.get("action", "none"))
            self.toggle_special_mode()
            return

        self.special_mode_var.set("Keyboard Combo")
        self.toggle_special_mode()
        keys = action_data.get("key", [])

        mod1 = "None"
        mod2 = "None"
        main_key = "A"

        if len(keys) == 1:
            main_key = keys[0]
        elif len(keys) == 2:
            mod1 = keys[0]
            main_key = keys[1]
        elif len(keys) >= 3:
            mod1 = keys[0]
            mod2 = keys[1]
            main_key = keys[-1]

        self.special_mod1_var.set(mod1.capitalize() if mod1 != "windows" else "windows")
        self.special_mod2_var.set(mod2.capitalize() if mod2 != "windows" else "windows")
        self.special_key_var.set(self._to_ui_key_label(main_key))

    def save_special_config(self):
        """Save selected special key action to special-keyout.json."""
        action_label = self.special_action_var.get()
        action_id = self.special_action_options.get(action_label)
        if not action_id:
            messagebox.showerror("Error", "Please select a valid special action.")
            return

        action_name = self.special_name_box.get("1.0", "end-1c").strip() or action_label

        if self.special_mode_var.get() == "Internal Action":
            ok = update_special_key(
                action_id,
                name=action_name,
                action_type=self.special_internal_action_var.get(),
            )
        else:
            keys = []
            if self.special_mod1_var.get() != "None":
                keys.append(self._normalize_key_token(self.special_mod1_var.get()))
            if self.special_mod2_var.get() != "None":
                mod2 = self._normalize_key_token(self.special_mod2_var.get())
                if mod2 not in keys:
                    keys.append(mod2)
            main_key = self._normalize_key_token(self.special_key_var.get())
            keys.append(main_key)

            ok = update_special_key(action_id, new_keys=keys, name=action_name)

        if ok:
            messagebox.showinfo("Saved", f"Updated {action_label}")
        else:
            messagebox.showerror("Error", "Failed to update special key configuration")

    def get_selected_profile(self):
        """
        Return the selected profile index. 
        Update mapping as needed for your profile buttons.
        """
        # Example mapping of profile names to indices based on your keyout.py
        profile_map = {
            "Default": 0,
            "Photoshop": 5,   # Adjust if needed
            "Pre Pro": 2,     # ...
            "Blender": 3,
            "Custom-1": 4,
            "Custom-2": 1
        }
        # Currently hardcoded to "Default" or you could store the selected profile from ProfilesSection
        return profile_map.get("Default", 0)

    def sync_modifiers(self, event=None):
        """Sample logic for sync. Not strictly required unless you're handling advanced combos."""
        first = self.first_modifier_var.get()
        second = self.second_modifier_var.get()
        options = ["None", "Ctrl", "Alt", "Shift", "windows"]  # Added "windows" to the options
        
        if first != "None" and second == first:
            self.second_modifier_var.set("None")
        
        second_options = options.copy()
        if first != "None" and first in second_options:
            second_options.remove(first)
        self.modifier_dropdown_2["values"] = second_options

        first_options = options.copy()
        if second != "None" and second in first_options:
            first_options.remove(second)
        self.modifier_dropdown_1["values"] = first_options

    def update_key_dropdowns(self):
        """Update the dropdown configuration based on radio button selection"""
        num_keys = self.key_combo_var.get()
        
        # Reset all dropdowns
        for widget in self.dropdown_frame.winfo_children():
            widget.pack_forget()
        
        if num_keys == 2:
            # Show only 2 dropdowns (first modifier and main key)
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")
            
            # First key (modifier)
            self.first_modifier_label.pack(pady=(5,2))
            self.modifier_dropdown_1.pack(pady=(0,3))
            
            # Second key (main key)
            self.third_key_label.pack(pady=(5,2))
            self.third_dropdown.pack(pady=(0,5))
            
        else:  # num_keys == 3
            # Show all 3 dropdowns (centered)
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")
            
            # First modifier label and dropdown
            self.first_modifier_label.pack(pady=(5,2))
            self.modifier_dropdown_1.pack(pady=(0,3))
            
            # Second modifier label and dropdown
            self.second_modifier_label.pack(pady=(5,2))
            self.modifier_dropdown_2.pack(pady=(0,3))
            
            # Main key label and dropdown
            self.third_key_label.pack(pady=(5,2))
            self.third_dropdown.pack(pady=(0,5))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigPanel(root)
    root.mainloop()