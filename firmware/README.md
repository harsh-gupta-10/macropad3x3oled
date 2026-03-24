# 🎛️ MacroPad RP2040 — Firmware

<p align="center">
  <b>Custom CircuitPython firmware for a DIY 3×3 macro pad built on the RP2040</b>
</p>

<p align="center">
  <a href="https://circuitpython.org/"><img src="https://img.shields.io/badge/CircuitPython-9.x-blueviolet?logo=python&logoColor=white" alt="CircuitPython"></a>
  <a href="https://www.raspberrypi.com/products/rp2040/"><img src="https://img.shields.io/badge/MCU-RP2040-green?logo=raspberrypi&logoColor=white" alt="RP2040"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"></a>
</p>

> **Companion Software →** [MacroPad Configurator (Python + Tkinter)](https://github.com/harsh-gupta-10/macropad-software-python-tkinter)

---

## ✨ Features

| Feature | Details |
|---|---|
| **9-Key Matrix** | 3×3 cherry-style key grid with full per-key configurability |
| **6 Profiles** | Each profile stores 9 independent key actions, switchable on the fly |
| **OLED Display** | SH1106 128×64 showing profile selector bubbles + logo icon previews |
| **2 Rotary Encoders** | Volume control + profile navigation with rotate / click / hold actions |
| **Mic Toggle** | Dedicated button for mic mute (default: F13) |
| **JSON-Driven Config** | All key mappings and settings live in editable JSON files on the drive |

### Action Types

- ⌨️ **Keyboard Shortcuts** — single key or multi-key combo (e.g. `Ctrl+Shift+Esc`)
- 🚀 **Launch Software** — opens any app via Windows search (e.g. `notepad`, `chrome`)
- 📝 **Text Macros** — type text in single / line-by-line / paragraph mode, with optional Shift+Enter for apps like WhatsApp
- 🔊 **Media Controls** — volume up/down, mute, play/pause

---

## 📁 Project Structure

```text
├── code.py               # Main CircuitPython loop (display, matrix, encoders)
├── keyout.py             # Action engine (combos, software launch, text typing)
├── keysfile.json         # Profile + key action definitions (9 keys × 6 profiles)
├── special-keyout.json   # Encoder & mic button mappings
├── img/                  # BMP icons for OLED profile preview
│   ├── youtube-logo-bmp.bmp
│   ├── vscode-logo-bmp.bmp
│   ├── obs-logo-bmp.bmp
│   ├── volt-logo-bmp.bmp
│   ├── windows-logo-bmp.bmp
│   └── photoshop-logo-bmp.bmp
├── lib/                  # CircuitPython libraries
│   ├── adafruit_hid/
│   ├── adafruit_display_text/
│   ├── adafruit_displayio_sh1106.mpy
│   └── ...
├── main.py               # Legacy KMK firmware (inactive when code.py exists)
└── settings.toml         # CircuitPython board settings
```

---

## 🔌 Hardware Wiring

### OLED Display (SH1106, I2C, address `0x3C`)

| Signal | Pin |
|--------|-----|
| SCL | GP9 |
| SDA | GP8 |

### Encoder 1 — Volume

| Signal | Pin |
|--------|-----|
| A / B | GP14, GP15 |
| Button | GP17 |

### Encoder 2 — Display / Profile (Software Quadrature)

| Signal | Pin |
|--------|-----|
| A / B | GP18, GP19 |
| Button | GP20 |

### Mic Toggle Button

| Signal | Pin |
|--------|-----|
| Button | GP0 |

### 3×3 Key Matrix

| | GP1 (Col 0) | GP2 (Col 1) | GP3 (Col 2) |
|---|---|---|---|
| **GP4 (Row 0)** | Key 1 | Key 4 | Key 7 |
| **GP13 (Row 1)** | Key 3 | Key 6 | Key 9 |
| **GP6 (Row 2)** | Key 2 | Key 5 | Key 8 |

> 💡 If a physical button maps to the wrong action, edit `key_mapping` in `code.py` — don't rearrange `keysfile.json`.

---

## 🎮 Controls

| Input | Action |
|---|---|
| Encoder 1 — Rotate | Volume Up / Down |
| Encoder 1 — Click | Play / Pause |
| Encoder 1 — Hold (1s) | Mute |
| Encoder 2 — Rotate | Previous / Next Profile |
| Encoder 2 — Click | Switch Profile (shows icon for 1s) |
| Encoder 2 — Hold (1s) | Configurable special action |
| Mic Button | Toggle mic (default: F13) |
| Matrix Keys 1–9 | Execute current profile action |

---

## ⚙️ Configuration

### Profile Keys — `keysfile.json`

```json
{
  "settings": {
    "active_profiles": 6,
    "encoder_speeds": { "volume": 3, "display": 1 }
  },
  "profiles": {
    "0": {
      "1": { "name": "Close Tab", "key": ["ctrl", "w"] },
      "2": { "name": "Open VS Code", "key": ["windows"], "software": "vscode" },
      "3": {
        "name": "WhatsApp Msg",
        "key": ["text_input"],
        "action": "text_input",
        "text_content": "Hello!\nHow are you?",
        "text_type": "paragraph",
        "text_press_enter": true,
        "text_shift_enter": true
      }
    }
  }
}
```

**Action Formats:**

| Type | Required Fields |
|---|---|
| Key Combo | `key: ["ctrl", "s"]` |
| Software Launch | `key: ["windows"]`, `software: "notepad"` |
| Text Input | `action: "text_input"`, `text_content`, `text_type` (`single` / `line-by-line` / `paragraph`) |

> **`text_shift_enter: true`** — uses Shift+Enter for newlines instead of Enter. Essential for WhatsApp and similar apps where Enter sends the message.

### Special Inputs — `special-keyout.json`

```json
{
  "special_keys": {
    "volume_encoder_left":  { "name": "Volume Down", "key": ["media_volume_down"] },
    "display_encoder_right": { "name": "Next Profile", "action": "profile_next" }
  }
}
```

Each entry uses either `"key"` (keyboard/media token) or `"action"` (`profile_next`, `profile_prev`, `none`).

---

## 🚀 Getting Started

1. **Flash CircuitPython** onto your RP2040 board ([circuitpython.org](https://circuitpython.org/))
2. **Copy all project files** to the `CIRCUITPY` drive root
3. **Copy the `lib/` folder** to `CIRCUITPY/lib/`
4. **Edit your configs** — `keysfile.json` for key actions, `special-keyout.json` for encoders
5. **Save and go** — the board auto-reloads on file changes

> Use the companion [MacroPad Configurator](https://github.com/harsh-gupta-10/macropad-software-python-tkinter) app to edit profiles visually instead of hand-editing JSON.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| No key output | Confirm USB HID is detected by the OS. Check token spelling in JSON. |
| Wrong button mapping | Adjust `key_mapping` dict in `code.py` |
| Display not showing | Verify I2C wiring (GP9/GP8) and OLED address (`0x3C`) |
| Special actions not updating | Validate `special-keyout.json` syntax |
| Serial debug | Connect via serial console (e.g. PuTTY, `screen`) at 115200 baud |

---

## 📝 Notes

- Optimized for **Windows** shortcuts and search-bar-based software launching.
- `main.py` contains a legacy KMK firmware path — it does **not** run while `code.py` is present.
- Unsupported key tokens are logged over serial for easy debugging.

---

## 📄 License

MIT © [Harsh Gupta](https://github.com/harsh-gupta-10)